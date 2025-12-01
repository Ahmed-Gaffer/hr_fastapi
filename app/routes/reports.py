# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\routes\reports.py
# File Name: reports.py
# -----------------------------------------

from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func
from app.database import get_session
from app.models.salary import SalaryRecord
from app.models.attendance import Attendance
from app.models.employee import Employee

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/salary")
def salary_report(session: Session = Depends(get_session)):
    """تقرير مجموع الرواتب حسب الشهر"""
    rows = session.exec(
        select(
            func.strftime("%Y-%m", SalaryRecord.paid_date).label("month"),
            func.sum(SalaryRecord.amount).label("total")
        )
        .group_by("month")
        .order_by("month")
    ).all()
    return [{"month": r[0], "total": r[1]} for r in rows]

@router.get("/attendance")
def attendance_stats(session: Session = Depends(get_session)):
    """إحصائيات الحضور"""
    total_emp = session.exec(select(func.count(Employee.id))).first() or 0
    rows = session.exec(
        select(Attendance.status, func.count(Attendance.id))
        .group_by(Attendance.status)
    ).all()

    stats = [{"name": r[0], "value": r[1]} for r in rows]
    present_count = next((r[1] for r in rows if r[0] == "حاضر"), 0)
    percent_present = (present_count / total_emp * 100) if total_emp else 0

    return {
        "stats": stats,
        "percent_present": round(percent_present, 1)
    }
