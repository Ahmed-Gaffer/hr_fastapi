from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date


class EmployeeRole(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالأدوار أو الصلاحيات (Many-to-Many)"""

    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)

    role_name: str  # اسم الدور (مثلاً: مشرف، مدير مشروع، مسؤول موارد بشرية)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
