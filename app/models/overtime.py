# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models/overtime.py
# File Name: overtime.py
# -----------------------------------------

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Overtime(SQLModel, table=True):
    """ساعات عمل إضافية (نهاري وليلي)"""
    __tablename__ = "overtime"

    id: Optional[int] = Field(default=None, primary_key=True)
    salary_id: int = Field(foreign_key="salary.id", index=True)

    # ⏰ نهاري
    day_hours: float = 0
    day_multiplier: float = 1.35
    day_amount: float = 0

    # 🌙 ليلي
    night_hours: float = 0
    night_multiplier: float = 1.7
    night_amount: float = 0

    # 💵 الإجمالي
    total_overtime_amount: float = 0

    created_at: datetime = Field(default_factory=datetime.utcnow)
