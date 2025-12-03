# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models/levels/level1/employee++/Employee_User.py
# File Name: Employee_User.py
# -----------------------------------------

from sqlmodel import SQLModel, Field
from typing import Optional

class EmployeeUser(SQLModel, table=True):
    """جدول وسيط يربط الموظف بحساب الدخول (User)"""
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    user_id: int = Field(foreign_key="user.id", index=True)

    role: str = "user"  # user أو admin
