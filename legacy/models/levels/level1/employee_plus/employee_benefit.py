# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level1\employee_plus\employee_benefit.py
# File Name: employee_benefit.py
# -----------------------------------------


from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models/levels/level1/employee++/employee_benefit.py
# File Name: employee_benefit.py
# -----------------------------------------

class EmployeeBenefit(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالبدلات"""
    __tablename__ = "employee_benefit"
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    benefit_id: int = Field(foreign_key="benefit.id", index=True)

    amount: Optional[float] = None
    notes: Optional[str] = None