from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level1\units\Reward.py
# File Name: Reward.py
# -----------------------------------------

class Reward(SQLModel, table=True):
    """المكافآت"""
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)

    reward_type: str  # مكافأة أداء، مكافأة مشروع
    amount: float
    reward_date: date
    notes: Optional[str] = None