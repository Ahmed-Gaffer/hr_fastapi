# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level1\employee_plus\employee_reward.py
# File Name: employee_reward.py
# -----------------------------------------



from sqlmodel import SQLModel, Field
from typing import Optional

class EmployeeReward(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالمكافآت"""
    __tablename__ = "employee_reward"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    reward_id: int = Field(foreign_key="reward.id", index=True)

    reason: Optional[str] = None