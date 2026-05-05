from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.dependencies.tenancy import get_current_tenant_from_header
from app.schemas.attendance import AttendanceCreate, AttendanceRead
from app.services.attendance_service import create_attendance
from app.models.attendance import Attendance

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post("/", response_model=AttendanceRead)
def create_attendance_route(
    payload: AttendanceCreate,
    session: Session = Depends(get_session),
    tenant = Depends(get_current_tenant_from_header),
):
    try:
        return create_attendance(session, tenant.id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[AttendanceRead])
def list_attendance(
    session: Session = Depends(get_session),
    tenant = Depends(get_current_tenant_from_header),
):
    records = session.exec(
        select(Attendance).where(Attendance.tenant_id == tenant.id)
    ).all()

    return records
