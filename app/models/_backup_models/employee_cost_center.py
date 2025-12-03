from typing import Optional
from sqlmodel import SQLModel, Field

class EmployeeCostcenter(SQLModel, table=True):
    """جدول وسيط يربط الموظف بمراكز التكلفة"""
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    cost_center_id: int = Field(foreign_key="costcenter.id", index=True)

    allocation_percentage: Optional[float] = None  # نسبة التوزيع
