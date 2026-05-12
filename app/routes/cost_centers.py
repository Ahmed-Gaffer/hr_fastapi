from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.database import get_session
from app.dependencies.dependencies import get_current_tenant
from app.models.cost_center import CostCenter

router = APIRouter(prefix="/cost-centers", tags=["cost-centers"])

@router.get("/")
def list_cost_centers(
    session: Session = Depends(get_session),
    tenant=Depends(get_current_tenant),
):
    return session.exec(select(CostCenter).where(CostCenter.tenant_id == tenant.id)).all()
