import os
import sys
import random
from datetime import date, datetime, timedelta

from sqlmodel import Session, select

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.database import engine
from app.models.department import Department
from app.models.employee import Employee
from app.models.site import Site
from app.models.cost_center import CostCenter
from app.models.salary import Salary, PayrollCategory
from app.models.attendance import Attendance
from app.models.tenant import Tenant


DEFAULT_DEPARTMENTS = [
    "الإدارة",
    "الموارد البشرية",
    "المبيعات",
    "التشغيل",
    "الهندسة",
    "المحاسبة",
]

STATUS_CHOICES = ["حاضر", "متأخر", "غائب"]


def choose_department(tenant_departments, employee):
    if employee.department_id:
        return employee.department_id
    if employee.job_title:
        title = employee.job_title.lower()
        for dept in tenant_departments:
            if any(keyword in title for keyword in ["موارد", "بشرية", "hr"]):
                if "الموارد" in dept.name:
                    return dept.id
            if any(keyword in title for keyword in ["مبيعات", "بيع", "sales"]):
                if "المبيعات" in dept.name:
                    return dept.id
            if any(keyword in title for keyword in ["محاس", "مالية", "account"]):
                if "المحاسبة" in dept.name:
                    return dept.id
            if any(keyword in title for keyword in ["هندسة", "مهندس", "engineering"]):
                if "الهندسة" in dept.name:
                    return dept.id
    return random.choice(tenant_departments).id if tenant_departments else None


def ensure_departments(session: Session, tenant: Tenant):
    existing = session.exec(
        select(Department).where(Department.tenant_id == tenant.id)
    ).all()
    if existing:
        return existing

    print(f"إنشاء أقسام افتراضية للعميل {tenant.name} (ID={tenant.id})")
    departments = []
    for name in DEFAULT_DEPARTMENTS:
        dept = Department(tenant_id=tenant.id, name=name)
        session.add(dept)
        departments.append(dept)
    session.commit()
    for dept in departments:
        session.refresh(dept)
    return departments


def fill_employee_departments(session: Session, tenant: Tenant, departments):
    employees = session.exec(
        select(Employee).where(Employee.tenant_id == tenant.id)
    ).all()
    updated = 0
    for emp in employees:
        if not emp.department_id:
            dept_id = choose_department(departments, emp)
            if dept_id:
                emp.department_id = dept_id
                session.add(emp)
                updated += 1
    if updated:
        session.commit()
    return len(employees), updated


def create_salary_records(session: Session, tenant: Tenant, employees):
    created = 0
    months = 6
    today = date.today()
    for emp in employees:
        has_salary = session.exec(
            select(Salary).where(Salary.employee_id == emp.id, Salary.tenant_id == tenant.id)
        ).first()
        if has_salary:
            continue

        for i in range(months):
            row_month = (today.month - i - 1) % 12 + 1
            row_year = today.year - ((today.month - i - 1) // 12)
            base = emp.base_salary or 10000
            allowance = round(base * random.uniform(0.05, 0.18), 2)
            overtime_amount = round(random.uniform(0, base * 0.08), 2)
            deductions = round(base * random.uniform(0.08, 0.16), 2)
            net = max(base + allowance + overtime_amount - deductions, base * 0.75)

            salary = Salary(
                tenant_id=tenant.id,
                employee_id=emp.id,
                cost_center_id=emp.cost_center_id,
                salary_year=row_year,
                salary_month=row_month,
                payroll_category=random.choice(list(PayrollCategory)),
                basic_salary=base,
                allowance_meals=round(allowance * 0.25, 2),
                allowance_transport=round(allowance * 0.3, 2),
                allowance_travel=round(allowance * 0.2, 2),
                allowance_cash=round(allowance * 0.25, 2),
                day_overtime_hours=random.randint(0, 10),
                night_overtime_hours=random.randint(0, 6),
                day_overtime_amount=round(overtime_amount * 0.6, 2),
                night_overtime_amount=round(overtime_amount * 0.4, 2),
                bonus_performance=round(base * random.uniform(0.02, 0.08), 2),
                bonus_project=round(base * random.uniform(0, 0.04), 2),
                other_earnings=round(base * random.uniform(0, 0.03), 2),
                total_earnings=round(base + allowance + overtime_amount, 2),
                deduction_insurance_social_employee=round(deductions * 0.35, 2),
                deduction_insurance_health=round(deductions * 0.25, 2),
                deduction_tax_income=round(deductions * 0.3, 2),
                deduction_absence=round(deductions * 0.1, 2),
                deduction_penalties=0,
                deduction_other=0,
                deduction_in_kind_benefits=0,
                total_deductions=round(deductions, 2),
                salary_due=round(base + allowance + overtime_amount - deductions, 2),
                advance_salary=0,
                loan_deduction=0,
                net_salary=round(net, 2),
                attendance_days=22,
                absence_days=random.randint(0, 2),
                payment_date=today,
                notes="بيانات راتب مولدة تلقائياً",
            )
            session.add(salary)
            created += 1
    session.commit()
    return created


def create_attendance_records(session: Session, tenant: Tenant, employees):
    created = 0
    days = 14
    today = date.today()
    for emp in employees:
        existing = session.exec(
            select(Attendance).where(Attendance.employee_id == emp.id)
        ).first()
        if existing:
            continue

        site_id = emp.site_id
        cost_center_id = emp.cost_center_id
        for d in range(days):
            record_date = today - timedelta(days=d)
            status = random.choices(STATUS_CHOICES, weights=[85, 10, 5], k=1)[0]
            attendance = Attendance(
                employee_id=emp.id,
                site_id=site_id,
                cost_center_id=cost_center_id,
                tenant_id=tenant.id,
                shift="الصباح",
                date=record_date,
                check_in=datetime(record_date.year, record_date.month, record_date.day, 8, random.randint(0, 15)).time(),
                check_out=datetime(record_date.year, record_date.month, record_date.day, 17, random.randint(0, 30)).time(),
                status=status,
            )
            session.add(attendance)
            created += 1
    session.commit()
    return created


def main():
    with Session(engine) as session:
        tenants = session.exec(select(Tenant)).all()
        if not tenants:
            print("لا يوجد بيانات مستأجرين في قاعدة البيانات.")
            return

        total_salary = 0
        total_attendance = 0
        total_employees = 0
        for tenant in tenants:
            departments = ensure_departments(session, tenant)
            employees = session.exec(
                select(Employee).where(Employee.tenant_id == tenant.id)
            ).all()
            total_employees += len(employees)
            employees_count, updated = fill_employee_departments(session, tenant, departments)
            salary_created = create_salary_records(session, tenant, employees)
            attendance_created = create_attendance_records(session, tenant, employees)
            total_salary += salary_created
            total_attendance += attendance_created
            print(
                f"Tenant {tenant.name} (ID={tenant.id}): {len(departments)} departments, "
                f"{employees_count} employees, {updated} department assignments, "
                f"{salary_created} salaries, {attendance_created} attendance records"
            )

        print(f"تم إنشاء {total_salary} سجل راتب و {total_attendance} سجل حضور لعدد {total_employees} موظف.")


if __name__ == "__main__":
    main()
