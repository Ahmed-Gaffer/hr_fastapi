from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.salary import SalaryRecord
from app.models.salary import PayrollCategory
from app.models.tenant import Tenant
from app.dependencies import get_current_tenant

router = APIRouter(prefix="/salary", tags=["salary"])

# 🔹 إضافة سجل راتب جديد
@router.post("/", response_model=SalaryRecord)
async def create_salary(
    record: SalaryRecord,
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant)
):
    """إضافة سجل راتب جديد لموظف"""
    record.tenant_id = tenant.id
    session.add(record)
    session.commit()
    session.refresh(record)
    return record

# 🔹 عرض كل الرواتب للشركة
@router.get("/", response_model=list[SalaryRecord])
async def list_salaries(
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant)
):
    """عرض كل الرواتب للشركة الحالية"""
    return session.exec(select(SalaryRecord).where(SalaryRecord.tenant_id == tenant.id)).all()

# 🔹 عرض راتب واحد
@router.get("/{salary_id}", response_model=SalaryRecord)
async def get_salary(
    salary_id: int,
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant)
):
    sal = session.exec(select(SalaryRecord).where(SalaryRecord.id == salary_id)).first()
    if not sal or sal.tenant_id != tenant.id:
        raise HTTPException(status_code=404, detail="الراتب غير موجود")
    return sal

# 🔹 تعديل راتب
@router.put("/{salary_id}", response_model=SalaryRecord)
async def update_salary(
    salary_id: int,
    data: SalaryRecord,
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant)
):
    sal = session.exec(select(SalaryRecord).where(SalaryRecord.id == salary_id)).first()
    if not sal or sal.tenant_id != tenant.id:
        raise HTTPException(status_code=404, detail="الراتب غير موجود")

    # تحديث الحقول الأساسية
    for field, value in data.dict(exclude_unset=True).items():
        setattr(sal, field, value)

    session.add(sal)
    session.commit()
    session.refresh(sal)
    return sal

# 🔹 حذف راتب
@router.delete("/{salary_id}")
async def delete_salary(
    salary_id: int,
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant)
):
    sal = session.exec(select(SalaryRecord).where(SalaryRecord.id == salary_id)).first()
    if not sal or sal.tenant_id != tenant.id:
        raise HTTPException(status_code=404, detail="الراتب غير موجود")
    session.delete(sal)
    session.commit()
    return {"detail": "تم حذف الراتب"}
