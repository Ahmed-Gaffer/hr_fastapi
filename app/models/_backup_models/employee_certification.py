# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models/levels/level1/employee++/employee_certification.py
# File Name: employee_certification.py
# -----------------------------------------

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date


class EmployeeCertification(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالشهادات المهنية (Many-to-Many)"""

    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)

    certificate_name: str  # اسم الشهادة (مثلاً: PMP، OSHA، CPA)
    issued_by: Optional[str] = None  # الجهة المانحة
    issue_date: Optional[date] = None
    expiry_date: Optional[date] = None
