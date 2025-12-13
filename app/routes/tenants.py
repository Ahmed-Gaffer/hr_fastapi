# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/routes\tenants.py
# File Name: tenants.py
# -----------------------------------------



import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.tenant import Tenant, TenantStatus
from app.models.company_config import CompanyConfig

router = APIRouter(prefix="/tenants", tags=["tenants"])

@router.post("/create")
async def create_tenant(
    name: str,
    code: str = None,   # ← اختياري
    industry: str = "مقاولات",
    owner_name: str = None,
    owner_email: str = None,
    session: Session = Depends(get_session)
):
    """إنشاء شركة جديدة"""

    # لو الكود مش مبعوت، يولّد واحد أوتوماتيك
    if not code:
        code = f"auto-{uuid.uuid4().hex[:6]}"

    # تحقق من عدم وجود كود مكرر
    existing = session.exec(select(Tenant).where(Tenant.code == code)).first()
    if existing:
        raise HTTPException(status_code=400, detail="الكود موجود بالفعل")

    tenant = Tenant(
        name=name,
        code=code,
        industry=industry,
        owner_name=owner_name,
        owner_email=owner_email,
        status=TenantStatus.ACTIVE,
        subscription_type="basic",
        subscription_start=datetime.utcnow(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        is_default=False
    )

    session.add(tenant)
    session.flush()

    # أنشئ إعدادات افتراضية للشركة
    config = CompanyConfig(tenant_id=tenant.id)
    session.add(config)
    session.commit()

    return {
        "id": tenant.id,
        "name": tenant.name,
        "code": tenant.code,
        "message": "تم إنشاء الشركة بنجاح"
    }

@router.get("/list")
async def list_tenants(session: Session = Depends(get_session)):
    """قائمة الشركات"""
    tenants = session.exec(select(Tenant)).all()
    return tenants

@router.get("/{tenant_id}")
async def get_tenant(tenant_id: int, session: Session = Depends(get_session)):
    """تفاصيل شركة"""
    tenant = session.exec(select(Tenant).where(Tenant.id == tenant_id)).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="الشركة غير موجودة")

    config = session.exec(select(CompanyConfig).where(CompanyConfig.tenant_id == tenant_id)).first()
    return {"tenant": tenant, "config": config}

@router.put("/{tenant_id}/config")
async def update_config(
    tenant_id: int,
    personal_exemption_annual: float = None,
    day_overtime_multiplier: float = None,
    night_overtime_multiplier: float = None,
    minimum_salary: float = None,
    session: Session = Depends(get_session)
):
    """تعديل إعدادات الشركة"""
    config = session.exec(select(CompanyConfig).where(CompanyConfig.tenant_id == tenant_id)).first()
    if not config:
        raise HTTPException(status_code=404, detail="الإعدادات غير موجودة")

    if personal_exemption_annual:
        config.personal_exemption_annual = personal_exemption_annual
    if day_overtime_multiplier:
        config.day_overtime_multiplier = day_overtime_multiplier
    if night_overtime_multiplier:
        config.night_overtime_multiplier = night_overtime_multiplier
    if minimum_salary is not None:
        config.minimum_salary = minimum_salary

    session.add(config)
    session.commit()
    return {"message": "تم تحديث الإعدادات"}