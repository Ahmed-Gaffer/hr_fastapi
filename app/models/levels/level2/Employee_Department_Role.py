# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level2\Employee_Department_Role.py
# File Name: Employee_Department_Role.py
# -----------------------------------------

from typing import Optional
from sqlmodel import SQLModel, Field

class Employeedepartmentrole(SQLModel, table=True):
    """جدول وسيط يربط القسم بالموظف والدور"""
    id: Optional[int] = Field(default=None, primary_key=True)
    department_id: int = Field(foreign_key="department.id", index=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    role_id: int = Field(foreign_key="employeerole.id", index=True)
    