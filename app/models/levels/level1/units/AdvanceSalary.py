# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level1\units\AdvanceSalary.py
# File Name: AdvanceSalary.py
# -----------------------------------------

class AdvanceSalary(SQLModel, table=True):
    """سلف الموظفين"""
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)

    amount: float
    request_date: date
    approved: bool = False
    approved_by: Optional[str] = None
    notes: Optional[str] = None