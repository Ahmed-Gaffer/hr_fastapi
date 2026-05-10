# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\public_holiday.py
# File Name: public_holiday.py
# -----------------------------------------



from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class PublicHoliday(SQLModel, table=True):
    """الإجازات الرسمية للشركة أو الدولة"""
    __tablename__ = "public_holiday"
    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(foreign_key="tenant.id", index=True)

    name: str  # اسم الإجازة (عيد، مناسبة وطنية)
    date: date
    is_paid: bool = True  # هل مدفوعة الأجر؟
    notes: Optional[str] = None