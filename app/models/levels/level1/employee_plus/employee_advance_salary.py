# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level1\employee_plus\employee_advance_salary.py
# File Name: employee_advance_salary.py
# -----------------------------------------



from sqlmodel import SQLModel, Field
from typing import Optional

class EmployeeAdvanceSalary(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالسلف"""
    __tablename__ = "employee_advance_salary"
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    advance_salary_id: int = Field(foreign_key="advance_salary.id", index=True)

    status: str = "قيد المراجعة"  # قيد المراجعة، موافق عليه، مرفوض