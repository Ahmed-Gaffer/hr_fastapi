from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level1\units\Loan.py
# File Name: Loan.py
# -----------------------------------------

class Loan(SQLModel, table=True):
    """قروض الموظفين"""
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)

    principal_amount: float  # أصل القرض
    interest_rate: float = 0.0
    start_date: date
    end_date: Optional[date] = None
    monthly_installment: float
    notes: Optional[str] = None