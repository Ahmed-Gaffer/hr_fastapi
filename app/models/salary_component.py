# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\salary_component.py
# File Name: salary_component.py
# -----------------------------------------


from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class ComponentType(str, Enum):
    """أنواع البنود الإضافية (مرونة للمستقبل)"""

    EXTRA_hOURS = "ساعات_إضافية"
    NIGHT_sHIFT = "عمل_ليلي"
    PERFORMANCE_bONUS = "مكافأة_أداء"
    PROJECT_bONUS = "مكافأة_مشروع"
    SITE_dEDUCTION = "خصم_موقع"
    OTHER_dEDUCTION = "خصم_آخر"
    OTHER_aLLOWANCE = "بدلة_أخرى"


class SalaryComponent(SQLModel, table=True):
    """بنود إضافية ومتغيرة في الراتب (ساعات إضافية، مكافآت، خصومات خاصة)"""

    __tablename__ = "salary_component"

    id: Optional[int] = Field(default=None, primary_key=True)

    # ✅ تصحيح اسم الجدول المرتبط
    salary_id: int = Field(
        foreign_key="salary.id",
        index=True
    )

    component_type: ComponentType  # نوع البند
    description: str  # وصف (مثلاً: "ساعات إضافية نهارية - 10 ساعات")
    quantity: float = 1  # الكمية (ساعات، أيام، إلخ)
    unit_rate: float  # السعر للوحدة
    amount: float  # الإجمالي = quantity × unit_rate
    is_deduction: bool = False  # True إذا كان خصم

    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        use_enum_values = True