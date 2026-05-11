from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select, func, and_
from sqlalchemy import desc
from app.database import get_session
from app.dependencies.dependencies import get_current_tenant
from app.models.tenant import Tenant
from app.models.employee import Employee
from app.models.salary import Salary
from app.models.attendance import Attendance
from app.models.department import Department
from app.models.site import Site
from app.models.cost_center import CostCenter

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/payroll-summary")
async def payroll_summary(
    year: int = Query(None),
    month: int = Query(None),
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant),
):
    """ملخص الرواتب حسب السنة والشهر"""
    query = select(
        Salary.salary_year,
        Salary.salary_month,
        func.count(Salary.id).label("employees_count"),
        func.sum(Salary.basic_salary).label("total_basic"),
        func.sum(Salary.total_earnings).label("total_earnings"),
        func.sum(Salary.total_deductions).label("total_deductions"),
        func.sum(Salary.net_salary).label("total_net"),
    ).where(Salary.tenant_id == tenant.id)

    if year:
        query = query.where(Salary.salary_year == year)
    if month:
        query = query.where(Salary.salary_month == month)

    query = query.group_by(Salary.salary_year, Salary.salary_month)
    query = query.order_by(desc(Salary.salary_year), desc(Salary.salary_month))

    results = session.exec(query).all()

    return [
        {
            "year": r[0],
            "month": r[1],
            "employees_count": r[2],
            "total_basic": float(r[3] or 0),
            "total_earnings": float(r[4] or 0),
            "total_deductions": float(r[5] or 0),
            "total_net": float(r[6] or 0),
        }
        for r in results
    ]


@router.get("/attendance-summary")
async def attendance_summary(
    from_date: str = Query(None),
    to_date: str = Query(None),
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant),
):
    """ملخص الحضور حسب الفترة الزمنية"""
    query = select(
        Attendance.date,
        Attendance.status,
        func.count(Attendance.id).label("count"),
    ).where(Attendance.tenant_id == tenant.id)

    if from_date:
        query = query.where(Attendance.date >= from_date)
    if to_date:
        query = query.where(Attendance.date <= to_date)

    query = query.group_by(Attendance.date, Attendance.status)
    query = query.order_by(desc(Attendance.date))

    results = session.exec(query).all()

    return [
        {
            "date": r[0],
            "status": r[1],
            "count": r[2],
        }
        for r in results
    ]


@router.get("/employee-performance")
async def employee_performance(
    year: int = Query(None),
    month: int = Query(None),
    department_id: int = Query(None),
    skip: int = Query(0),
    limit: int = Query(100),
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant),
):
    """تقرير أداء الموظفين حسب الرواتب والحضور"""
    query = select(
        Employee.id,
        Employee.name,
        Employee.code,
        func.count(Attendance.id).label("total_days"),
        func.sum((Attendance.status == "حاضر").cast(int)).label("present_days"),
        func.avg(Salary.net_salary).label("avg_salary"),
    ).join(
        Attendance, Attendance.employee_id == Employee.id, isouter=True
    ).join(
        Salary, Salary.employee_id == Employee.id, isouter=True
    ).where(Employee.tenant_id == tenant.id)

    if year and month:
        query = query.where(
            and_(
                Salary.salary_year == year,
                Salary.salary_month == month,
            )
        )

    if department_id:
        query = query.where(Employee.department_id == department_id)

    query = query.group_by(Employee.id, Employee.name, Employee.code)

    total = session.exec(query).all().__len__()
    results = session.exec(query.offset(skip).limit(limit)).all()

    return {
        "total": total,
        "results": [
            {
                "employee_id": r[0],
                "name": r[1],
                "code": r[2],
                "total_days": r[3],
                "present_days": r[4],
                "avg_salary": float(r[5] or 0),
                "attendance_rate": round((r[4] / r[3] * 100) if r[3] else 0, 2),
            }
            for r in results
        ],
    }


@router.get("/department-analysis")
async def department_analysis(
    year: int = Query(None),
    month: int = Query(None),
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant),
):
    """تحليل الأقسام حسب الرواتب وعدد الموظفين"""
    query = select(
        Department.id,
        Department.name,
        func.count(Employee.id).label("employees_count"),
        func.sum(Salary.net_salary).label("total_salaries"),
        func.avg(Salary.net_salary).label("avg_salary"),
    ).join(
        Employee, Employee.department_id == Department.id, isouter=True
    ).join(
        Salary, and_(
            Salary.employee_id == Employee.id,
        ), isouter=True
    ).where(Department.tenant_id == tenant.id)

    if year and month:
        query = query.where(
            and_(
                Salary.salary_year == year,
                Salary.salary_month == month,
            )
        )

    query = query.group_by(Department.id, Department.name)
    query = query.order_by(func.count(Employee.id).desc())

    results = session.exec(query).all()

    return [
        {
            "department_id": r[0],
            "department_name": r[1],
            "employees_count": r[2],
            "total_salaries": float(r[3] or 0),
            "avg_salary": float(r[4] or 0),
        }
        for r in results
    ]


@router.get("/cost-center-analysis")
async def cost_center_analysis(
    year: int = Query(None),
    month: int = Query(None),
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant),
):
    """تحليل مراكز التكلفة حسب الرواتب والموارد"""
    query = select(
        CostCenter.id,
        CostCenter.name,
        func.count(Employee.id).label("employees_count"),
        func.sum(Salary.net_salary).label("total_salaries"),
        func.sum(Salary.total_deductions).label("total_deductions"),
    ).join(
        Employee, Employee.cost_center_id == CostCenter.id, isouter=True
    ).join(
        Salary, Salary.employee_id == Employee.id, isouter=True
    ).where(CostCenter.tenant_id == tenant.id)

    if year and month:
        query = query.where(
            and_(
                Salary.salary_year == year,
                Salary.salary_month == month,
            )
        )

    query = query.group_by(CostCenter.id, CostCenter.name)
    query = query.order_by(func.sum(Salary.net_salary).desc())

    results = session.exec(query).all()

    return [
        {
            "cost_center_id": r[0],
            "cost_center_name": r[1],
            "employees_count": r[2],
            "total_salaries": float(r[3] or 0),
            "total_deductions": float(r[4] or 0),
        }
        for r in results
    ]
