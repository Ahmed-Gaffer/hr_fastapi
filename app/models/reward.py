# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\reward.py
# File Name: reward.py
# -----------------------------------------


from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import date

# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level1\units\Reward.py
# File Name: Reward.py
# -----------------------------------------

class Reward(SQLModel, table=True):
    """المكافآت"""
    __tablename__ = "reward"
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)

    reward_type: str  # مكافأة أداء، مكافأة مشروع
    amount: float
    reward_date: date
    notes: Optional[str] = None