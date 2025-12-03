# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models/levels/level1/employee++/Employee_Loan.py
# File Name: Employee_Loan.py
# -----------------------------------------

from sqlmodel import SQLModel, Field
from typing import Optional

class EmployeeLoan(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالقروض"""
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    loan_id: int = Field(foreign_key="loan.id", index=True)

    status: str = "نشط"  # نشط، مسدد، متأخر
