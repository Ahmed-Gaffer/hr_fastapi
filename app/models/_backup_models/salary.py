# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models/salary.py
# File Name: salary.py
# -----------------------------------------

from typing import Optional
from datetime import date, datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship


class Salary(str, Enum):
    CATEGORY_A = "الفئة_الأولى"
    CATEGORY_B = "الفئة_الثانية"
    CATEGORY_C = "الفئة_الثالثة"


class Salary(SQLModel, table=True):
    """سجل الراتب (مع Tenant)"""

    id: Optional[int] = Field(default=None, primary_key=True)

    # ⭐ Multi-tenancy
    tenant_id: int = Field(foreign_key="tenant.id", index=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    cost_center_id: Optional[int] = Field(foreign_key="costcenter.id", index=True)  # مركز التكلفة

    # 📅 الفترة
    salary_year: int
    salary_month: int
    payroll_category: Salary = Salary.CATEGORY_A

    # 💰 الاستحقاقات
    basic_salary: float = 0
    allowance_meals: float = 0
    allowance_transport: float = 0
    allowance_travel: float = 0
    allowance_cash: float = 0
    day_overtime_hours: float = 0
    night_overtime_hours: float = 0
    day_overtime_amount: float = 0
    night_overtime_amount: float = 0
    bonus_performance: float = 0
    bonus_project: float = 0
    other_earnings: float = 0
    total_earnings: float = 0

    # 📉 الاستقطاعات
    deduction_insurance_social_employee: float = 0
    deduction_insurance_health: float = 0
    deduction_tax_income: float = 0
    deduction_absence: float = 0
    deduction_penalties: float = 0
    deduction_other: float = 0
    deduction_in_kind_benefits: float = 0
    total_deductions: float = 0

    # 💵 الراتب المستحق
    salary_due: float = 0

    # 🏦 السلف والقروض
    advance_salary: float = 0
    loan_deduction: float = 0

    # ✅ الصافي النهائي
    net_salary: float = 0

    # 📌 معلومات إضافية
    attendance_days: int = 30
    absence_days: int = 0
    payment_date: Optional[date] = None
    notes: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # 🔗 علاقات ORM
    employee: "Employee" = Relationship(back_populates="salaries")
    cost_center: Optional["CostCenter"] = Relationship(back_populates="salaries")
    tenant: "Tenant" = Relationship(back_populates="salaries")
