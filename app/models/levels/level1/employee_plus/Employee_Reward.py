# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models/levels/level1/employee++/Employee_Reward.py
# File Name: Employee_Reward.py
# -----------------------------------------

from sqlmodel import SQLModel, Field
from typing import Optional

class Employee_Reward(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالمكافآت"""
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    reward_id: int = Field(foreign_key="reward.id", index=True)

    reason: Optional[str] = None
