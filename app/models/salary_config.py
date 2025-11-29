from sqlmodel import SQLModel, Field
from typing import Optional


class SalaryConfig(SQLModel, table=True):
    """إعدادات الرواتب والضرائب (سنة وشركة)"""

    id: Optional[int] = Field(default=None, primary_key=True)
    year: int = Field(index=True)

    # 🔧 معدلات التأمين
    insurance_social_employee_rate: float = 0.11  # 11%
    insurance_social_employer_rate: float = 0.19  # 19%
    insurance_health_rate: float = 0.02  # 2%

    # 💰 معدلات الضريبة
    tax_rate: float = 0.20  # 20%
    personal_exemption_annual: float = 15000  # إعفاء شخصي سنوي
    min_taxable_monthly: float = 3000  # الحد الأدنى الخاضع للضريبة

    # 📅 إعدادات الحضور
    standard_working_days: int = 30
    standard_working_hours: float = 240  # 8 ساعات × 30 يوم

    # 🎯 معدل الساعات الإضافية
    extra_hours_multiplier: float = 1.5
    night_shift_multiplier: float = 1.75  # عمل ليلي = 175% من الأجر

    # 📌 ملاحظات
    description: Optional[str] = None

    class Config:
        unique_constraint = [("year",)]
