from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.database import get_session
from app.dependencies.dependencies import get_current_tenant
from app.models.department import Department

router = APIRouter(prefix="/departments", tags=["departments"])

@router.get("/")
def list_departments(
    session: Session = Depends(get_session),
    tenant=Depends(get_current_tenant),
):
    return session.exec(select(Department).where(Department.tenant_id == tenant.id)).all()
