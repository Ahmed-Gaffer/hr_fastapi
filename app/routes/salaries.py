from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.dependencies.tenancy import get_current_tenant_from_header
from app.schemas.salary import SalaryCreate, SalaryRead
from app.services.salary_service import create_salary
from app.models.salary import Salary

router = APIRouter(prefix="/salaries", tags=["Salaries"])


@router.post("/", response_model=SalaryRead)
def create_salary_route(
    payload: SalaryCreate,
    session: Session = Depends(get_session),
    tenant = Depends(get_current_tenant_from_header),
):
    try:
        return create_salary(session, tenant.id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[SalaryRead])
def list_salaries(
    session: Session = Depends(get_session),
    tenant = Depends(get_current_tenant_from_header),
):
    salaries = session.exec(
        select(Salary).where(Salary.tenant_id == tenant.id)
    ).all()

    return salaries
