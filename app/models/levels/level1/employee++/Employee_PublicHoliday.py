# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models/levels/level1/employee++/Employee_PublicHoliday.py
# File Name: Employee_PublicHoliday.py
# -----------------------------------------

from sqlmodel import SQLModel, Field
from typing import Optional

class EmployeeHoliday(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالإجازات الرسمية"""
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    holiday_id: int = Field(foreign_key="publicholiday.id", index=True)

    is_paid: bool = True
    notes: Optional[str] = None
