from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class OvertimeRecord(SQLModel, table=True):
    """ساعات عمل إضافية (نهاري وليلي)"""

    id: Optional[int] = Field(default=None, primary_key=True)
    salary_record_id: int = Field(foreign_key="salaryrecord.id", index=True)

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
