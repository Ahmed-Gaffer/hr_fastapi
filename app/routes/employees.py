from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.dependencies.dependencies import get_current_tenant
from app.models.employee import Employee, EmployeeCreate, EmployeeStatus, EmployeeUpdate
from app.models.tenant import Tenant


router = APIRouter(prefix="/employees", tags=["employees"])


def employee_payload(emp: Employee) -> dict:
    return {
        "id": emp.id,
        "tenant_id": emp.tenant_id,
        "site_id": emp.site_id,
        "cost_center_id": emp.cost_center_id,
        "department_id": emp.department_id,
        "code": emp.code,
        "name": emp.name,
        "national_id": emp.national_id,
        "job_title": emp.job_title,
        "hire_date": emp.hire_date,
        "base_salary": emp.base_salary,
        "employee_category": emp.employee_category,
        "insurance_status": emp.insurance_status,
        "work_status": emp.work_status,
        "status": emp.status,
        "site_name": emp.site.name if emp.site else None,
        "cost_center_name": emp.cost_center.name if emp.cost_center else None,
        "department_name": emp.department.name if emp.department else None,
    }


@router.post("/", response_model=dict)
async def create_employee(
    employee: EmployeeCreate,
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant),
):
    exists = session.exec(
        select(Employee).where(
            Employee.tenant_id == tenant.id,
            Employee.code == employee.code,
        )
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail="Employee code already exists")

    emp = Employee(
        tenant_id=tenant.id,
        site_id=employee.site_id,
        cost_center_id=employee.cost_center_id,
        department_id=employee.department_id,
        code=employee.code,
        name=employee.name,
        national_id=employee.national_id,
        job_title=employee.job_title,
        hire_date=employee.hire_date,
        base_salary=employee.base_salary,
        employee_category=employee.employee_category,
        insurance_status=employee.insurance_status,
        work_status=employee.work_status,
        status=employee.status or EmployeeStatus.ACTIVE,
    )
    session.add(emp)
    session.commit()
    session.refresh(emp)
    return employee_payload(emp)


@router.get("/", response_model=list[dict])
async def list_employees(
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant),
):
    employees = session.exec(
        select(Employee).where(Employee.tenant_id == tenant.id)
    ).all()
    return [employee_payload(emp) for emp in employees]


@router.get("/{employee_id}", response_model=dict)
async def get_employee(
    employee_id: int,
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant),
):
    emp = session.exec(select(Employee).where(Employee.id == employee_id)).first()
    if not emp or emp.tenant_id != tenant.id:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee_payload(emp)


@router.put("/{employee_id}", response_model=dict)
async def update_employee(
    employee_id: int,
    data: EmployeeUpdate,
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant),
):
    emp = session.exec(select(Employee).where(Employee.id == employee_id)).first()
    if not emp or emp.tenant_id != tenant.id:
        raise HTTPException(status_code=404, detail="Employee not found")

    if data.code and data.code != emp.code:
        other = session.exec(
            select(Employee).where(
                Employee.tenant_id == tenant.id,
                Employee.code == data.code,
                Employee.id != employee_id,
            )
        ).first()
        if other:
            raise HTTPException(status_code=400, detail="Employee code already exists")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(emp, field, value)

    session.add(emp)
    session.commit()
    session.refresh(emp)
    return employee_payload(emp)


@router.delete("/{employee_id}")
async def delete_employee(
    employee_id: int,
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant),
):
    emp = session.exec(select(Employee).where(Employee.id == employee_id)).first()
    if not emp or emp.tenant_id != tenant.id:
        raise HTTPException(status_code=404, detail="Employee not found")
    session.delete(emp)
    session.commit()
    return {"detail": "Employee deleted"}
