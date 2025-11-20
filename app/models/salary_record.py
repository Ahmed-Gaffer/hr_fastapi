from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, datetime
from enum import Enum

class PayrollCategory(str, Enum):
    CATEGORY_A = "الفئة_الأولى"
    CATEGORY_B = "الفئة_الثانية"

class SalaryRecord(SQLModel, table=True):
    """سجل الراتب (مع Tenant)"""
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # ⭐ Multi-tenancy
    tenant_id: int = Field(foreign_key="tenant.id", index=True)
    
    employee_id: int = Field(foreign_key="employee.id", index=True)
    salary_year: int
    salary_month: int
    payroll_category: PayrollCategory = PayrollCategory.CATEGORY_A
    
    # الاستحقاقات
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
    
    # الاستقطاعات
    deduction_insurance_social_employee: float = 0
    deduction_insurance_health: float = 0
    deduction_tax_income: float = 0
    deduction_absence: float = 0
    deduction_penalties: float = 0
    deduction_other: float = 0
    deduction_in_kind_benefits: float = 0  # خصم البدلات العينية
    total_deductions: float = 0
    
    # الراتب المستحق
    salary_due: float = 0
    
    # السلف والقروض
    advance_salary: float = 0
    loan_deduction: float = 0
    
    # الصافي النهائي
    net_salary: float = 0
    
    # معلومات إضافية
    attendance_days: int = 30
    absence_days: int = 0
    payment_date: Optional[date] = None
    notes: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    __table_args__ = (
        {"indexes": [
            "tenant_id, employee_id, salary_year, salary_month",
        ]},
    )