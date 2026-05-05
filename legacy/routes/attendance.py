# راوتر خاص بالحضور
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select
from app.database import get_session
from app.models.attendance import Attendance
from app.models.employee import Employee

router = APIRouter(prefix="/attendance", tags=["attendance"])


# دالة تعرض الحضور كـ HTML (لـ HTMX)
@router.get("/list", response_class=HTMLResponse)
def list_attendance_htmx(session: Session = Depends(get_session)):
    records = session.exec(select(Attendance)).all()

    html = "<ul class='space-y-2'>"

    for r in records:
        html += (
            f"<li class='p-2 border rounded bg-gray-50'>"
            f"📅 {r.date} - 👤 موظف رقم {r.employee_id} "
            f"- دخول: {r.check_in} - خروج: {r.check_out}"
            f"</li>"
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
@router.get("/", response_model=list[dict])
def list_attendance(session: Session = Depends(get_session)):
    records = session.exec(select(Attendance)).all()

    result = []
    for r in records:
        employee_name = "N/A"
        if r.employee_id:
            emp = session.exec(
                select(Employee).where(Employee.id == r.employee_id)
            ).first()
            if emp:
                employee_name = emp.name

        result.append(
            {
                "id": r.id,
                "employee_name": employee_name,
                "date": r.date,
                "status": r.status,
            }
        )

    return result
