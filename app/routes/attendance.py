# راوتر خاص بالحضور
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select
from app.database import get_session
from app.models.attendance import Attendance
from app.models.employee import Employee
from datetime import datetime

router = APIRouter(prefix="/attendance", tags=["attendance"])

# دالة تعرض الحضور كـ HTML (لـ HTMX)
@router.get("/list", response_class=HTMLResponse)
def list_attendance_htmx(session: Session = Depends(get_session)):
    records = session.exec(select(Attendance)).all()  # جلب كل سجلات الحضور

    # بناء HTML بسيط لعرضهم
    html = "<ul class='space-y-2'>"
    for record in records:
        # عرض اسم الموظف وتاريخ الحضور ووقت الدخول والخروج
        html += (
            f"<li class='p-2 border rounded bg-gray-50'>"
            f"📅 {record.date} - 👤 موظف رقم {record.employee_id} "
            f"- دخول: {record.check_in} - خروج: {record.check_out}</li>"
        )
    html += "</ul>"
    return html

# دالة لإضافة سجل حضور
@router.post("/", response_model=Attendance)
def check_in(att: Attendance, session: Session = Depends(get_session)):
    session.add(att)
    session.commit()
    session.refresh(att)
    return att

# دالة لعرض كل سجلات الحضور
@router.get("/", response_model=list[Attendance])
def list_attendance(session: Session = Depends(get_session)):
    records = session.exec(select(Attendance)).all()
    return [
        {
            "id": r.id,
            "employee_name": session.exec(
                select(Employee).where(Employee.id == r.employee_id)
            ).first().name if r.employee_id else "N/A",
            "date": r.date,
            "status": r.status,
        }
        for r in records
    ]
