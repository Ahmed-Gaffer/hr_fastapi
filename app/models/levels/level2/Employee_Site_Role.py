# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level2\Employee_Site_Role.py
# File Name: Employee_Site_Role.py
# -----------------------------------------

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class Employeesiterole(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالموقع والدور"""
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    site_id: int = Field(foreign_key="site.id", index=True)
    role_id: int = Field(foreign_key="employeerole.id", index=True)

    start_date: Optional[date] = None
    end_date: Optional[date] = None
