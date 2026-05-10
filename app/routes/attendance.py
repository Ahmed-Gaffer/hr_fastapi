from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select

from app.database import get_session
from app.dependencies.dependencies import get_current_tenant
from app.models.attendance import Attendance, AttendanceCreate
from app.models.employee import Employee
from app.models.tenant import Tenant


router = APIRouter(prefix="/attendance", tags=["attendance"])


def attendance_payload(record: Attendance) -> dict:
    return {
        "id": record.id,
        "tenant_id": record.tenant_id,
        "employee_id": record.employee_id,
        "employee_name": record.employee.name if record.employee else None,
        "site_id": record.site_id,
        "site_name": record.site.name if record.site else None,
        "cost_center_id": record.cost_center_id,
        "cost_center_name": record.cost_center.name if record.cost_center else None,
        "date": record.date,
        "check_in": record.check_in,
        "check_out": record.check_out,
        "status": record.status,
    }


@router.get("/list", response_class=HTMLResponse)
def list_attendance_htmx(
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant),
):
    records = session.exec(
        select(Attendance).where(Attendance.tenant_id == tenant.id)
    ).all()

    html = "<ul class='space-y-2'>"
    for record in records:
        html += (
            f"<li class='p-2 border rounded bg-gray-50'>"
            f"{record.date} - employee #{record.employee_id} "
            f"- in: {record.check_in} - out: {record.check_out}"
            f"</li>"
        )
    html += "</ul>"
    return html


@router.post("/", response_model=dict)
def create_attendance(
    data: AttendanceCreate,
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant),
):
    employee = session.exec(
        select(Employee).where(
            Employee.id == data.employee_id,
            Employee.tenant_id == tenant.id,
        )
    ).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    record = Attendance(
        tenant_id=tenant.id,
        employee_id=employee.id,
        site_id=data.site_id if data.site_id is not None else employee.site_id,
        cost_center_id=(
            data.cost_center_id
            if data.cost_center_id is not None
            else employee.cost_center_id
        ),
        date=data.date,
        check_in=data.check_in,
        check_out=data.check_out,
        status=data.status or "حاضر",
    )
    session.add(record)
    session.commit()
    session.refresh(record)
    return attendance_payload(record)


@router.get("/", response_model=list[dict])
def list_attendance(
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant),
):
    records = session.exec(
        select(Attendance).where(Attendance.tenant_id == tenant.id)
    ).all()
    return [attendance_payload(record) for record in records]
