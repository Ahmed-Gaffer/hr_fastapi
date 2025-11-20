# ...تعديل الموجود...
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.employee import Employee
from app.models.tenant import Tenant
from app.dependencies import get_current_tenant

router = APIRouter(prefix="/employees", tags=["employees"])

@router.post("/create")
async def create_employee(
    name: str,
    code: str,
    base_salary: float,
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant)
):
    """إنشاء موظف (ضمن الشركة الحالية)"""
    
    # تحقق من عدم تكرار الكود ضمن الشركة
    existing = session.exec(
        select(Employee).where(
            Employee.tenant_id == tenant.id,
            Employee.code == code
        )
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="الكود موجود بالفعل في هذه الشركة")
    
    emp = Employee(
        tenant_id=tenant.id,
        name=name,
        code=code,
        base_salary=base_salary,
        status="نشط"
    )
    
    session.add(emp)
    session.commit()
    
    return {"id": emp.id, "message": "تم إنشاء الموظف"}

@router.get("/list")
async def list_employees(
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant)
):
    """قائمة الموظفين (الشركة الحالية فقط)"""
    employees = session.exec(
        select(Employee).where(Employee.tenant_id == tenant.id)
    ).all()
    return employees