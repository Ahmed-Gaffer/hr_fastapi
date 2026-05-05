# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/services\employee_service.py
# File Name: employee_service.py
# -----------------------------------------

from datetime import datetime
from sqlmodel import Session, select
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


def create_employee(
    session: Session,
    tenant_id: int,
    data: EmployeeCreate
) -> Employee:

    # تأكد إن الكود مش مستخدم في نفس الشركة
    existing = session.exec(
        select(Employee).where(
            Employee.tenant_id == tenant_id,
            Employee.code == data.code
        )
    ).first()

    if existing:
        raise ValueError("كود الموظف مستخدم بالفعل")

    employee = Employee(
        tenant_id=tenant_id,
        code=data.code,
        name=data.name,
        national_id=data.national_id,
        job_title=data.job_title,
        hire_date=data.hire_date,
        base_salary=data.base_salary or 0.0,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    session.add(employee)
    session.commit()
    session.refresh(employee)

    return employee


def update_employee(
    session: Session,
    tenant_id: int,
    employee_id: int,
    data: EmployeeUpdate
) -> Employee:

    employee = session.get(Employee, employee_id)

    if not employee or employee.tenant_id != tenant_id:
        raise ValueError("الموظف غير موجود")

    # تحديث آمن
    for field, value in data.dict(exclude_none=True).items():
        setattr(employee, field, value)

    employee.updated_at = datetime.utcnow()

    session.add(employee)
    session.commit()
    session.refresh(employee)

    return employee