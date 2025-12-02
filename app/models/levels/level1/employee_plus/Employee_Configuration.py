# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models/levels/level1/employee++/Employee_Configuration.py
# File Name: Employee_Configuration.py
# -----------------------------------------

from sqlmodel import SQLModel, Field
from typing import Optional

class Employee_Configuration(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالإعدادات"""
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    config_id: int = Field(foreign_key="configuration.id", index=True)

    value: Optional[str] = None
