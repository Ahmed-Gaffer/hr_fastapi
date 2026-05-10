from fastapi import APIRouter, Depends
from sqlmodel import Session, func, select

from app.database import get_session
from app.dependencies.dependencies import get_current_tenant
from app.models.attendance import Attendance
from app.models.employee import Employee
from app.models.salary import Salary
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
