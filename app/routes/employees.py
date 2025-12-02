# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\routes\employees.py
# File Name: employees.py
# -----------------------------------------

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.employee import Employee, EmployeeCreate, EmployeeUpdate
from app.models.tenant import Tenant
from app.dependencies.dependencies import get_current_tenant

router = APIRouter(prefix="/employees", tags=["employees"])

@router.post("/", response_model=Employee)
async def create_employee(
    employee: EmployeeCreate,
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant)
):
    exists = session.exec(
        select(Employee).where(Employee.tenant_id == tenant.id, Employee.code == employee.code)
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail="موظف بنفس الكود موجود بالفعل")

    emp = Employee(
        tenant_id=tenant.id,
        name=employee.name,
        code=employee.code,
        base_salary=employee.base_salary,
        status=employee.status or "نشط",
        department=employee.department
    )
    session.add(emp)
    session.commit()
    session.refresh(emp)
    return emp

@router.get("/", response_model=list[Employee])
async def list_employees(
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant)
):
    return session.exec(select(Employee).where(Employee.tenant_id == tenant.id)).all()

@router.get("/{employee_id}", response_model=Employee)
async def get_employee(
    employee_id: int,
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant)
):
    emp = session.exec(select(Employee).where(Employee.id == employee_id)).first()
    if not emp or emp.tenant_id != tenant.id:
        raise HTTPException(status_code=404, detail="الموظف غير موجود")
    return emp

@router.put("/{employee_id}", response_model=Employee)
async def update_employee(
    employee_id: int,
    data: EmployeeUpdate,
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant)
):
    emp = session.exec(select(Employee).where(Employee.id == employee_id)).first()
    if not emp or emp.tenant_id != tenant.id:
        raise HTTPException(status_code=404, detail="الموظف غير موجود")

    if data.code and data.code != emp.code:
        other = session.exec(
            select(Employee).where(Employee.tenant_id == tenant.id, Employee.code == data.code, Employee.id != employee_id)
        ).first()
        if other:
            raise HTTPException(status_code=400, detail="كود مستخدم من قبل موظف آخر")

    # تحديث انتقائي
    emp.name = data.name or emp.name
    emp.code = data.code or emp.code
    emp.base_salary = data.base_salary if data.base_salary is not None else emp.base_salary
    emp.status = data.status or emp.status
    emp.department = data.department or emp.department

    session.add(emp)
    session.commit()
    session.refresh(emp)
    return emp

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
