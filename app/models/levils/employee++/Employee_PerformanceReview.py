from sqlmodel import SQLModel, Field
from typing import Optional

class EmployeePerformance(SQLModel, table=True):
    """جدول وسيط يربط الموظف بتقييمات الأداء"""
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    review_id: int = Field(foreign_key="performancereview.id", index=True)

    final_score: Optional[float] = None
