from sqlmodel import Session, select
from datetime import datetime, date

from app.models.salary import Salary
from app.models.employee import Employee
from app.schemas.salary import SalaryCreate


def calculate_net_salary(
    base: float,
    overtime: float,
    bonuses: float,
    deductions: float
) -> float:
    return round(base + overtime + bonuses - deductions, 2)


def create_salary(
    session: Session,
    tenant_id: int,
    data: SalaryCreate
) -> Salary:

    # تأكد إن الموظف تابع لنفس الشركة
    employee = session.exec(
        select(Employee).where(
            Employee.id == data.employee_id,
            Employee.tenant_id == tenant_id
        )
    ).first()

    if not employee:
        raise ValueError("الموظف غير موجود في هذه الشركة")

    # منع تكرار مرتب نفس الشهر
    existing = session.exec(
        select(Salary).where(
            Salary.employee_id == data.employee_id,
            Salary.month == data.month
        )
    ).first()

    if existing:
        raise ValueError("تم تسجيل مرتب لهذا الشهر بالفعل")

    base_salary = employee.base_salary

    net_salary = calculate_net_salary(
        base=base_salary,
        overtime=data.overtime or 0.0,
        bonuses=data.bonuses or 0.0,
        deductions=data.deductions or 0.0
    )

    salary = Salary(
        tenant_id=tenant_id,
        employee_id=data.employee_id,
        month=data.month,
        base_salary=base_salary,
        overtime=data.overtime or 0.0,
        bonuses=data.bonuses or 0.0,
        deductions=data.deductions or 0.0,
        net_salary=net_salary,
        created_at=datetime.utcnow()
    )

    session.add(salary)
    session.commit()
    session.refresh(salary)

    return salary
