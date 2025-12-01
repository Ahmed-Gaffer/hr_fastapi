# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models/company_config.py
# File Name: company_config.py
# -----------------------------------------

from sqlmodel import SQLModel, Field
from typing import Optional
import json


class CompanyConfig(SQLModel, table=True):
    """إعدادات الشركة المخصصة"""

    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(foreign_key="tenant.id", index=True, unique=True)

    # 🔧 إعدادات الراتب
    personal_exemption_annual: float = 15000  # الإعفاء الشخصي السنوي
    insurance_social_employee_rate: float = 0.10  # 10%
    insurance_health_rate: float = 0.0  # سيُحسب ديناميكياً حسب الموظف
    insurance_employer_social_rate: float = 0.1475  # 14.75%
    insurance_employer_health_rate: float = 0.04  # 4% (للمحافظات المشمولة)

    # 🔧 إعدادات الساعات الإضافية
    day_overtime_multiplier: float = 1.35
    night_overtime_multiplier: float = 1.7

    # 🔧 إعدادات الغياب
    absence_deduction_type: str = "percentage"  # percentage أو fixed
    absence_deduction_value: float = 1.0  # نسبة أو قيمة ثابتة

    # 🔧 إعدادات الحد الأدنى للراتب
    minimum_salary_enabled: bool = True
    minimum_salary: float = 0

    # 🔧 البدلات الإجبارية
    default_in_kind_benefits: str = Field(
        default=json.dumps({
            "meals": True,
            "transport": True,
            "travel": True
        })
    )

    # 🔧 إعدادات الضريبة (JSON للمرونة)
    tax_policy_config: str = Field(
        default=json.dumps({
            "enabled": True,
            "type": "progressive"
        })
    )

    # 🔧 إعدادات السلف والقروض
    advance_salary_enabled: bool = True
    advance_salary_max_percentage: float = 0.5  # 50% من الراتب
    loan_enabled: bool = True

    # 🔧 إعدادات العطلات والإجازات
    annual_leave_days: int = 21
    sick_leave_days: int = 10
    public_holidays_days: int = 7

    # 🔧 إعدادات التقارير والإشعارات
    salary_slip_format: str = "pdf"  # pdf, excel, html
    send_salary_notifications: bool = True
    notification_days_before: int = 3  # قبل يوم الصرف ب 3 أيام

    # 🔧 المحافظات المشمولة بالتأمين الشامل (JSON)
    comprehensive_insurance_governorates: str = Field(
        default=json.dumps([
            "الأقصر", "بورسعيد", "الإسماعيلية", "السويس",
            "البحر الأحمر", "مطروح", "أسوان", "الإسكندرية",
            "البحيرة", "دمياط", "سوهاج", "شمال سيناء",
            "جنوب سيناء", "قنا", "كفر الشيخ"
        ])
    )

    notes: Optional[str] = None

    # 🛠️ دوال مساعدة لتحويل JSON إلى dict/list
    def get_default_benefits(self) -> dict:
        return json.loads(self.default_in_kind_benefits)

    def get_tax_config(self) -> dict:
        return json.loads(self.tax_policy_config)

    def get_comprehensive_insurance_governorates(self) -> list:
        return json.loads(self.comprehensive_insurance_governorates)
