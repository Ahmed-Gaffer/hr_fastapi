# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level1\employee_plus\employee_disciplinary.py
# File Name: employee_disciplinary.py
# -----------------------------------------



from sqlmodel import SQLModel, Field
from typing import Optional

class EmployeeDisciplinary(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالعقوبات"""
    __tablename__ = "employee_disciplinary"
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    disciplinary_action_id: int = Field(foreign_key="disciplinary_action.id", index=True)

    severity: Optional[str] = None  # بسيطة، متوسطة، شديدة