# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/routes\system.py
# File Name: system.py
# -----------------------------------------



from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.company_config import CompanyConfig
from app.models.tenant import Tenant
from app.dependencies.dependencies import get_current_tenant

router = APIRouter(prefix="/system", tags=["system"])

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/config", response_model=CompanyConfig)
async def get_config(
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant)
):
    config = session.exec(
        select(CompanyConfig).where(CompanyConfig.tenant_id == tenant.id)
    ).first()
    if not config:
        config = CompanyConfig(tenant_id=tenant.id)
        session.add(config)
        session.commit()
        session.refresh(config)
    return config

@router.put("/config", response_model=CompanyConfig)
async def update_config(
    config_data: CompanyConfig,
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant)
):
    config = session.exec(
        select(CompanyConfig).where(CompanyConfig.tenant_id == tenant.id)
    ).first()
    if not config:
        config = CompanyConfig(tenant_id=tenant.id)
        session.add(config)
    for key, value in config_data.dict(exclude_unset=True).items():
        if key != 'id' and key != 'tenant_id':
            setattr(config, key, value)
    session.commit()
    session.refresh(config)
    return config