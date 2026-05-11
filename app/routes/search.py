from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, or_
from app.database import get_session
from app.dependencies.dependencies import get_current_tenant
from app.models.tenant import Tenant
from app.models.employee import Employee
from app.models.salary import Salary
from app.models.attendance import Attendance
from app.models.department import Department

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/employees")
async def search_employees(
    q: str = Query("", description="البحث عن الموظفين"),
    department_id: int = Query(None, description="تصفية حسب القسم"),
    site_id: int = Query(None, description="تصفية حسب الموقع"),
    cost_center_id: int = Query(None, description="تصفية حسب مركز التكلفة"),
    status: str = Query(None, description="تصفية حسب الحالة"),
    skip: int = Query(0),
    limit: int = Query(50),
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant),
):
    """البحث والفلترة المتقدمة للموظفين"""
    query = select(Employee).where(Employee.tenant_id == tenant.id)

    if q:
        query = query.where(
            or_(
                Employee.name.contains(q),
                Employee.code.contains(q),
                Employee.national_id.contains(q),
                Employee.job_title.contains(q),
            )
        )

    if department_id:
        query = query.where(Employee.department_id == department_id)
    if site_id:
        query = query.where(Employee.site_id == site_id)
    if cost_center_id:
        query = query.where(Employee.cost_center_id == cost_center_id)
    if status:
        query = query.where(Employee.status == status)

    total = session.exec(query).all().__len__()
    results = session.exec(query.offset(skip).limit(limit)).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "results": [
            {
                "id": e.id,
                "code": e.code,
                "name": e.name,
                "job_title": e.job_title,
                "status": e.status,
                "department_id": e.department_id,
                "department_name": e.department.name if e.department else None,
                "site_id": e.site_id,
                "site_name": e.site.name if e.site else None,
                "cost_center_id": e.cost_center_id,
                "cost_center_name": e.cost_center.name if e.cost_center else None,
                "base_salary": e.base_salary,
            }
            for e in results
        ],
    }


@router.get("/salaries")
async def search_salaries(
    employee_id: int = Query(None, description="تصفية حسب الموظف"),
    year: int = Query(None, description="السنة"),
    month: int = Query(None, description="الشهر"),
    min_salary: float = Query(None, description="الحد الأدنى للراتب"),
    max_salary: float = Query(None, description="الحد الأقصى للراتب"),
    skip: int = Query(0),
    limit: int = Query(50),
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant),
):
    """البحث والفلترة المتقدمة للرواتب"""
    query = select(Salary).where(Salary.tenant_id == tenant.id)

    if employee_id:
        query = query.where(Salary.employee_id == employee_id)
    if year:
        query = query.where(Salary.salary_year == year)
    if month:
        query = query.where(Salary.salary_month == month)
    if min_salary:
        query = query.where(Salary.net_salary >= min_salary)
    if max_salary:
        query = query.where(Salary.net_salary <= max_salary)

    total = session.exec(query).all().__len__()
    results = session.exec(query.order_by(Salary.salary_year.desc(), Salary.salary_month.desc()).offset(skip).limit(limit)).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "results": [
            {
                "id": s.id,
                "employee_id": s.employee_id,
                "employee_name": s.employee.name if s.employee else None,
                "year": s.salary_year,
                "month": s.salary_month,
                "basic_salary": s.basic_salary,
                "total_earnings": s.total_earnings,
                "total_deductions": s.total_deductions,
                "net_salary": s.net_salary,
            }
            for s in results
        ],
    }


@router.get("/attendance")
async def search_attendance(
    employee_id: int = Query(None, description="تصفية حسب الموظف"),
    status: str = Query(None, description="تصفية حسب الحالة"),
    from_date: str = Query(None, description="من التاريخ (YYYY-MM-DD)"),
    to_date: str = Query(None, description="إلى التاريخ (YYYY-MM-DD)"),
    skip: int = Query(0),
    limit: int = Query(50),
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant),
):
    """البحث والفلترة المتقدمة للحضور"""
    query = select(Attendance).where(Attendance.tenant_id == tenant.id)

    if employee_id:
        query = query.where(Attendance.employee_id == employee_id)
    if status:
        query = query.where(Attendance.status == status)
    if from_date:
        query = query.where(Attendance.date >= from_date)
    if to_date:
        query = query.where(Attendance.date <= to_date)

    total = session.exec(query).all().__len__()
    results = session.exec(query.order_by(Attendance.date.desc()).offset(skip).limit(limit)).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "results": [
            {
                "id": a.id,
                "employee_id": a.employee_id,
                "employee_name": a.employee.name if a.employee else None,
                "date": a.date,
                "check_in": a.check_in,
                "check_out": a.check_out,
                "status": a.status,
                "site_name": a.site.name if a.site else None,
                "cost_center_name": a.cost_center.name if a.cost_center else None,
            }
            for a in results
        ],
    }
