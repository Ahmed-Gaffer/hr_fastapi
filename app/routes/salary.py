# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\routes\salary.py
# File Name: salary.py
# -----------------------------------------

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.salary import Salary
from app.models.salary import PayrollCategory
from app.models.tenant import Tenant
from app.dependencies.dependencies import get_current_tenant

router = APIRouter(prefix="/salary", tags=["salary"])

# 🔹 إضافة سجل راتب جديد
@router.post("/", response_model=Salary)
async def create_salary(
    : Salary,
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant)
):
    """إضافة سجل راتب جديد لموظف"""
    .tenant_id = tenant.id
    session.add()
    session.commit()
    session.refresh()
    return 

# 🔹 عرض كل الرواتب للشركة
@router.get("/", response_model=list[Salary])
async def list_salaries(
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant)
):
    """عرض كل الرواتب للشركة الحالية"""
    return session.exec(select(Salary).where(Salary.tenant_id == tenant.id)).all()

# 🔹 عرض راتب واحد
@router.get("/{salary_id}", response_model=Salary)
async def get_salary(
    salary_id: int,
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant)
):
    sal = session.exec(select(Salary).where(Salary.id == salary_id)).first()
    if not sal or sal.tenant_id != tenant.id:
        raise HTTPException(status_code=404, detail="الراتب غير موجود")
    return sal

# 🔹 تعديل راتب
@router.put("/{salary_id}", response_model=Salary)
async def update_salary(
    salary_id: int,
    data: Salary,
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant)
):
    sal = session.exec(select(Salary).where(Salary.id == salary_id)).first()
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
    sal = session.exec(select(Salary).where(Salary.id == salary_id)).first()
    if not sal or sal.tenant_id != tenant.id:
        raise HTTPException(status_code=404, detail="الراتب غير موجود")
    session.delete(sal)
    session.commit()
    return {"detail": "تم حذف الراتب"}
