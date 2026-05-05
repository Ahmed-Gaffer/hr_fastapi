from sqlmodel import Session, select
from app.models.attendance import Attendance
from app.models.employee import Employee
from app.schemas.attendance import AttendanceCreate
from datetime import datetime


def create_attendance(
    session: Session,
    tenant_id: int,
    data: AttendanceCreate
) -> Attendance:

    # تأكد إن الموظف تبع نفس الشركة
    employee = session.exec(
        select(Employee).where(
            Employee.id == data.employee_id,
            Employee.tenant_id == tenant_id
        )
    ).first()

    if not employee:
        raise ValueError("الموظف غير موجود في هذه الشركة")

    # منع تكرار نفس اليوم
    existing = session.exec(
        select(Attendance).where(
            Attendance.employee_id == data.employee_id,
            Attendance.date == data.date
        )
    ).first()

    if existing:
        raise ValueError("تم تسجيل حضور لهذا اليوم بالفعل")

    attendance = Attendance(
        tenant_id=tenant_id,
        employee_id=data.employee_id,
        date=data.date,
        check_in=data.check_in,
        check_out=data.check_out,
        status=data.status or "present",
        shift=data.shift,
        created_at=datetime.utcnow()
    )

    session.add(attendance)
    session.commit()
    session.refresh(attendance)

    return attendance
