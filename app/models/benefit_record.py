from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum

class BenefitType(str, Enum):
    """نوع البدلة"""
    IN_KIND_MEALS = "وجبات"
    IN_KIND_TRANSPORT = "مواصلات"
    IN_KIND_TRAVEL = "سفر"
    CASH_ALLOWANCE = "بدلة نقدية"

class BenefitRecord(SQLModel, table=True):
    """تسجيل البدلات (في النوع والقيمة)"""
    id: Optional[int] = Field(default=None, primary_key=True)
    salary_record_id: int = Field(foreign_key="salaryrecord.id", index=True)
    
    benefit_type: BenefitType
    description: str
    amount: float
    is_cash: bool  # True = نقد فعلي، False = عيني (سيُخصم لاحقاً)