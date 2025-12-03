# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models/salary_component.py
# File Name: salary_component.py
# -----------------------------------------

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class SalaryComponent(str, Enum):
    """أنواع البنود الإضافية (مرونة للمستقبل)"""
    EXTRA_HOURS = "ساعات_إضافية"
    NIGHT_SHIFT = "عمل_ليلي"
    PERFORMANCE_BONUS = "مكافأة_أداء"
    PROJECT_BONUS = "مكافأة_مشروع"
    SITE_DEDUCTION = "خصم_موقع"
    OTHER_DEDUCTION = "خصم_آخر"
    OTHER_ALLOWANCE = "بدلة_أخرى"


class Salarycomponent(SQLModel, table=True):
    """بنود إضافية ومتغيرة في الراتب (ساعات إضافية، مكافآت، خصومات خاصة)"""

    id: Optional[int] = Field(default=None, primary_key=True)
    salary_record_id: int = Field(foreign_key="salaryrecord.id", index=True)

    component_type: ComponentType  # نوع البند
    description: str  # وصف (مثلاً: "ساعات إضافية نهارية - 10 ساعات")
    quantity: float = 1  # الكمية (ساعات، أيام، إلخ)
    unit_rate: float  # السعر للوحدة
    amount: float  # الإجمالي = quantity × unit_rate
    is_deduction: bool = False  # True إذا كان خصم

    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        use_enum_values = True
