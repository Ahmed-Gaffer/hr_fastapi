from sqlmodel import SQLModel, Field
from typing import Optional

class EmployeeDisciplinary(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالعقوبات"""
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    action_id: int = Field(foreign_key="disciplinaryaction.id", index=True)

    severity: Optional[str] = None  # بسيطة، متوسطة، شديدة
