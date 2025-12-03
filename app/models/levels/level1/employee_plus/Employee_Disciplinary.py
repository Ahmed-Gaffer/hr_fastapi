# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models/levels/level1/employee++/Employee_Disciplinary.py
# File Name: Employee_Disciplinary.py
# -----------------------------------------

from sqlmodel import SQLModel, Field
from typing import Optional

class Employeedisciplinary(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالعقوبات"""
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    action_id: int = Field(foreign_key="disciplinaryaction.id", index=True)

    severity: Optional[str] = None  # بسيطة، متوسطة، شديدة
