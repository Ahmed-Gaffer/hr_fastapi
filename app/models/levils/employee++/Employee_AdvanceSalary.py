from sqlmodel import SQLModel, Field
from typing import Optional, Field

class EmployeeAdvance(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالسلف"""
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    advance_id: int = Field(foreign_key="advancesalary.id", index=True)

    status: str = "قيد المراجعة"  # قيد المراجعة، موافق عليه، مرفوض
