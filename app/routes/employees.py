# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/routes\employees.py
# File Name: employees.py
# -----------------------------------------

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.dependencies.tenancy import get_current_tenant_from_header
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeRead
)
from app.services.employee_service import (
    create_employee,
    update_employee
)
from app.models.employee import Employee

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post("/", response_model=EmployeeRead)
def create_employee_route(
    payload: EmployeeCreate,
    session: Session = Depends(get_session),
    tenant = Depends(get_current_tenant_from_header),
):
    try:
        return create_employee(session, tenant.id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[EmployeeRead])
def list_employees(
    session: Session = Depends(get_session),
    tenant = Depends(get_current_tenant_from_header),
):
    employees = session.exec(
        select(Employee).where(Employee.tenant_id == tenant.id)
    ).all()

    return employees


@router.put("/{employee_id}", response_model=EmployeeRead)
def update_employee_route(
    employee_id: int,
    payload: EmployeeUpdate,
    session: Session = Depends(get_session),
    tenant = Depends(get_current_tenant_from_header),
):
    try:
        return update_employee(session, tenant.id, employee_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))