# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models/levels/level1/employee++/Employee_SalaryRecord.py
# File Name: Employee_SalaryRecord.py
# -----------------------------------------

from sqlmodel import SQLModel, Field
from typing import Optional

class Employeesalaryrecord(SQLModel, table=True):
    """جدول وسيط يربط الموظف بسجلات الرواتب"""
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    salary_id: int = Field(foreign_key="salaryrecord.id", index=True)

    effective_from: Optional[date] = None
    effective_to: Optional[date] = None
