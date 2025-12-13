# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level1\employee_plus\employee_salary.py
# File Name: employee_salary.py
# -----------------------------------------



from sqlmodel import SQLModel, Field
from typing import Optional

class EmployeeSalary(SQLModel, table=True):
    """جدول وسيط يربط الموظف بسجلات الرواتب"""
    __tablename__ = "employee_salary"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    salary_id: int = Field(foreign_key="salary.id", index=True)

    effective_from: Optional[date] = None
    effective_to: Optional[date] = None