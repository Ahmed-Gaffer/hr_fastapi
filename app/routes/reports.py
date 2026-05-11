from fastapi import APIRouter, Depends
from sqlmodel import Session, func, select

from app.database import get_session
from app.dependencies.dependencies import get_current_tenant
from app.models.attendance import Attendance
from app.models.cost_center import CostCenter
from app.models.department import Department
from app.models.employee import Employee
from app.models.overtime import Overtime
from app.models.salary import Salary
from app.models.site import Site
from app.models.tenant import Tenant


router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/salary")
def salary_report(
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant),
):
    rows = session.exec(
        select(
            Salary.salary_year,
            Salary.salary_month,
            func.sum(Salary.net_salary),
        )
        .where(Salary.tenant_id == tenant.id)
        .group_by(Salary.salary_year, Salary.salary_month)
        .order_by(Salary.salary_year, Salary.salary_month)
    ).all()

    return [
        {
            "month": f"{year}-{month:02d}",
            "total": float(total or 0),
        }
        for year, month, total in rows
    ]


@router.get("/attendance")
def attendance_stats(
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant),
):
    total_emp = session.exec(
        select(func.count(Employee.id)).where(Employee.tenant_id == tenant.id)
    ).first() or 0
    rows = session.exec(
        select(Attendance.status, func.count(Attendance.id))
        .where(Attendance.tenant_id == tenant.id)
        .group_by(Attendance.status)
    ).all()

    stats = [{"name": status, "value": count} for status, count in rows]
    present_count = next((count for status, count in rows if status == "حاضر"), 0)
    percent_present = (present_count / total_emp * 100) if total_emp else 0

    return {
        "stats": stats,
        "percent_present": round(percent_present, 1),
    }


@router.get("/salary/by-department")
def salary_by_department(
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant),
):
    rows = session.exec(
        select(
            Department.name,
            func.sum(Salary.net_salary),
        )
        .join(Employee, Salary.employee_id == Employee.id)
        .join(Department, Employee.department_id == Department.id)
        .where(Salary.tenant_id == tenant.id)
        .group_by(Department.name)
        .order_by(Department.name)
    ).all()

    return [
        {"name": name or "غير محدد", "value": float(total or 0)}
        for name, total in rows
    ]


@router.get("/salary/by-cost-center")
def salary_by_cost_center(
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant),
):
    rows = session.exec(
        select(
            CostCenter.name,
            func.sum(Salary.net_salary),
        )
        .join(CostCenter, CostCenter.id == Salary.cost_center_id)
        .where(Salary.tenant_id == tenant.id)
        .group_by(CostCenter.name)
        .order_by(CostCenter.name)
    ).all()

    return [
        {"name": name or "غير محدد", "value": float(total or 0)}
        for name, total in rows
    ]


@router.get("/attendance/by-site")
def attendance_by_site(
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant),
):
    rows = session.exec(
        select(Site.name, func.count(Attendance.id))
        .join(Site, Site.id == Attendance.site_id)
        .where(Attendance.tenant_id == tenant.id)
        .group_by(Site.name)
        .order_by(Site.name)
    ).all()

    return [{"name": name or "غير محدد", "value": int(count)} for name, count in rows]


@router.get("/employees/by-department")
def employees_by_department(
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant),
):
    rows = session.exec(
        select(Department.name, func.count(Employee.id))
        .join(Department, Department.id == Employee.department_id)
        .where(Employee.tenant_id == tenant.id)
        .group_by(Department.name)
        .order_by(Department.name)
    ).all()

    return [{"name": name or "غير محدد", "value": int(count)} for name, count in rows]


@router.get("/employees/by-site")
def employees_by_site(
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant),
):
    rows = session.exec(
        select(Site.name, func.count(Employee.id))
        .join(Employee, Employee.site_id == Site.id)
        .where(Employee.tenant_id == tenant.id)
        .group_by(Site.name)
        .order_by(Site.name)
    ).all()

    return [{"name": name or "بدون موقع", "value": int(count)} for name, count in rows]


@router.get("/employees/by-cost-center")
def employees_by_cost_center(
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant),
):
    rows = session.exec(
        select(CostCenter.name, func.count(Employee.id))
        .join(Employee, Employee.cost_center_id == CostCenter.id)
        .where(Employee.tenant_id == tenant.id)
        .group_by(CostCenter.name)
        .order_by(CostCenter.name)
    ).all()

    return [{"name": name or "غير محدد", "value": int(count)} for name, count in rows]


@router.get("/employees/by-job-title")
def employees_by_job_title(
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant),
):
    rows = session.exec(
        select(Employee.job_title, func.count(Employee.id))
        .where(Employee.tenant_id == tenant.id)
        .group_by(Employee.job_title)
        .order_by(Employee.job_title)
    ).all()

    return [{"name": title or "غير محدد", "value": int(count)} for title, count in rows]


@router.get("/employees/without-department")
def employees_without_department(
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant),
):
    missing_count = session.exec(
        select(func.count(Employee.id))
        .where(Employee.tenant_id == tenant.id, Employee.department_id == None)
    ).first() or 0
    with_count = session.exec(
        select(func.count(Employee.id))
        .where(Employee.tenant_id == tenant.id, Employee.department_id != None)
    ).first() or 0

    return [
        {"name": "بدون قسم", "value": int(missing_count)},
        {"name": "مع قسم", "value": int(with_count)},
    ]


@router.get("/attendance/by-cost-center")
def attendance_by_cost_center(
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant),
):
    rows = session.exec(
        select(CostCenter.name, func.count(Attendance.id))
        .join(CostCenter, CostCenter.id == Attendance.cost_center_id)
        .where(Attendance.tenant_id == tenant.id)
        .group_by(CostCenter.name)
        .order_by(CostCenter.name)
    ).all()

    return [{"name": name or "غير محدد", "value": int(count)} for name, count in rows]


@router.get("/salary/by-site")
def salary_by_site(
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant),
):
    rows = session.exec(
        select(Site.name, func.sum(Salary.net_salary))
        .join(Employee, Salary.employee_id == Employee.id)
        .join(Site, Employee.site_id == Site.id)
        .where(Salary.tenant_id == tenant.id)
        .group_by(Site.name)
        .order_by(Site.name)
    ).all()

    return [{"name": name or "غير محدد", "value": float(total or 0)} for name, total in rows]


@router.get("/overtime/summary")
def overtime_summary(
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant),
):
    rows = session.exec(
        select(
            Salary.salary_year,
            Salary.salary_month,
            func.sum(Overtime.total_overtime_amount),
        )
        .join(Overtime, Overtime.salary_id == Salary.id)
        .where(Salary.tenant_id == tenant.id)
        .group_by(Salary.salary_year, Salary.salary_month)
        .order_by(Salary.salary_year, Salary.salary_month)
    ).all()

    return [
        {"month": f"{year}-{month:02d}", "value": float(total or 0)}
        for year, month, total in rows
    ]

