# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\routes\salary_components.py
# File Name: salary_components.py
# -----------------------------------------

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.salary_component import SalaryComponent, ComponentType
from app.models.salary import SalaryRecord
from app.models.tenant import Tenant
from app.dependencies.dependencies import get_current_tenant

router = APIRouter(prefix="/salary-components", tags=["salary-components"])

# 🔹 إضافة بند جديد للراتب
@router.post("/", response_model=SalaryComponent)
async def add_component(
    component: SalaryComponent,
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant)
):
    """إضافة بند إضافي أو خصم مرتبط بسجل راتب"""
    record = session.exec(
        select(SalaryRecord).where(SalaryRecord.id == component.salary_record_id)
    ).first()
    if not record or record.tenant_id != tenant.id:
        raise HTTPException(status_code=404, detail="سجل الراتب غير موجود أو لا يخص هذه الشركة")

    session.add(component)
    session.commit()
    session.refresh(component)
    return component

# 🔹 عرض البنود المرتبطة بسجل راتب
@router.get("/{salary_record_id}", response_model=list[SalaryComponent])
async def list_components(
    salary_record_id: int,
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant)
):
    """عرض كل البنود المرتبطة بسجل راتب معين"""
    record = session.exec(
        select(SalaryRecord).where(SalaryRecord.id == salary_record_id)
    ).first()
    if not record or record.tenant_id != tenant.id:
        raise HTTPException(status_code=404, detail="سجل الراتب غير موجود أو لا يخص هذه الشركة")

    return session.exec(
        select(SalaryComponent).where(SalaryComponent.salary_record_id == salary_record_id)
    ).all()

# 🔹 حذف بند
@router.delete("/{component_id}")
async def delete_component(
    component_id: int,
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant)
):
    comp = session.exec(select(SalaryComponent).where(SalaryComponent.id == component_id)).first()
    if not comp:
        raise HTTPException(status_code=404, detail="البند غير موجود")
    # تأكد إن البند مرتبط بسجل راتب لنفس الشركة
    record = session.exec(select(SalaryRecord).where(SalaryRecord.id == comp.salary_record_id)).first()
    if not record or record.tenant_id != tenant.id:
        raise HTTPException(status_code=403, detail="غير مسموح بحذف بند من شركة أخرى")

    session.delete(comp)
    session.commit()
    return {"detail": "تم حذف البند"}
