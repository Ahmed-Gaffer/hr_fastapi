# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/dependencies\dependencies.py
# File Name: dependencies.py
# -----------------------------------------



from typing import Optional
from fastapi import Header, HTTPException, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.models.tenant import Tenant
from app.core.context import set_current_tenant

async def get_current_tenant(
    x_tenant_id: Optional[int] = Header(None, description="معرّف الشركة"),
    session: Session = Depends(get_session)
) -> Tenant:
    """
    احصل على الشركة الحالية من الـ header.
    إذا لم يُرسَل X-Tenant-ID، يستخدم الشركة الافتراضية رقم 1.
    """
    if x_tenant_id is None:
        x_tenant_id = 1

    tenant = session.exec(
        select(Tenant).where(Tenant.id == x_tenant_id)
    ).first()
    
    if not tenant:
        raise HTTPException(status_code=404, detail="الشركة غير موجودة")
    
    if tenant.status == "معطل":
        raise HTTPException(status_code=403, detail="الشركة معطلة")
    
    set_current_tenant(x_tenant_id)
    return tenant

async def get_company_config(
    tenant: Tenant = Depends(get_current_tenant),
    session: Session = Depends(get_session)
):
    """احصل على إعدادات الشركة"""
    from app.models.company_config import CompanyConfig
    config = session.exec(
        select(CompanyConfig).where(CompanyConfig.tenant_id == tenant.id)
    ).first()
    
    if not config:
        # أنشئ config افتراضي
        config = CompanyConfig(tenant_id=tenant.id)
        session.add(config)
        session.commit()
    
    return config