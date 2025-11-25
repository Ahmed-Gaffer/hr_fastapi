# app/routes/employees.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.employee import Employee
from app.models.tenant import Tenant
from app.dependencies import get_current_tenant

router = APIRouter(prefix="/employees", tags=["employees"])

# 🔹 إنشاء موظف جديد
@router.post("/create", response_model=Employee)
async def create_employee(
    name: str,
    code: str,
    base_salary: float,
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant)
):
    """إنشاء موظف جديد ضمن الشركة الحالية"""
    existing = session.exec(
        select(Employee).where(
            Employee.tenant_id == tenant.id,
            Employee.code == code
        )
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="موظف بنفس الكود موجود بالفعل")

    emp = Employee(
        tenant_id=tenant.id,
        name=name,
        code=code,
        base_salary=base_salary,
        status="نشط"
    )
    session.add(emp)
    session.commit()
    session.refresh(emp)
    return emp

# 🔹 قائمة الموظفين
@router.get("/list", response_model=list[Employee])
async def list_employees(
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant)
):
    """عرض جميع الموظفين للشركة الحالية"""
    employees = session.exec(
        select(Employee).where(Employee.tenant_id == tenant.id)
    ).all()
    return employees

# 🔹 عرض موظف واحد
@router.get("/{employee_id}", response_model=Employee)
async def get_employee(
    employee_id: int,
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant)
):
    """عرض بيانات موظف واحد"""
    emp = session.exec(select(Employee).where(Employee.id == employee_id)).first()
    if not emp or emp.tenant_id != tenant.id:
        raise HTTPException(status_code=404, detail="الموظف غير موجود")
    return emp

# 🔹 تعديل بيانات موظف
@router.put("/{employee_id}", response_model=Employee)
async def update_employee(
    employee_id: int,
    name: str,
    code: str,
    base_salary: float,
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant)
):
    """تعديل بيانات الموظف"""
    emp = session.exec(select(Employee).where(Employee.id == employee_id)).first()
    if not emp or emp.tenant_id != tenant.id:
        raise HTTPException(status_code=404, detail="الموظف غير موجود")
    # تحقق من تكرار الكود مع موظف آخر
    other = session.exec(
        select(Employee).where(Employee.tenant_id == tenant.id, Employee.code == code, Employee.id != employee_id)
    ).first()
    if other:
        raise HTTPException(status_code=400, detail="كود مستخدم من قبل موظف آخر")

    emp.name = name
    emp.code = code
    emp.base_salary = base_salary
    session.add(emp)
    session.commit()
    session.refresh(emp)
    return emp

# 🔹 حذف موظف
@router.delete("/{employee_id}")
async def delete_employee(
    employee_id: int,
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant)
):
    emp = session.exec(select(Employee).where(Employee.id == employee_id)).first()
    if not emp or emp.tenant_id != tenant.id:
        raise HTTPException(status_code=404, detail="الموظف غير موجود")
    session.delete(emp)
    session.commit()
    return {"detail": "تم حذف الموظف"}
