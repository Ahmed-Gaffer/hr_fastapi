# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models/levels/level1/employee++/Employee_DeductionRecord.py
# File Name: Employee_DeductionRecord.py
# -----------------------------------------

from sqlmodel import SQLModel, Field
from typing import Optional

class Employeedeductionrecord(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالخصومات"""
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    deduction_id: int = Field(foreign_key="deductionrecord.id", index=True)

    amount: Optional[float] = None
    reason: Optional[str] = None
