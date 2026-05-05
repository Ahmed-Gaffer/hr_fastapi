from typing import Optional
from datetime import date, datetime
from sqlmodel import SQLModel, Field


class Salary(SQLModel, table=True):
    __tablename__ = "salaries"

    id: Optional[int] = Field(default=None, primary_key=True)

    tenant_id: int = Field(index=True)
    employee_id: int = Field(index=True)

    month: date  # أول يوم في الشهر (2025-01-01)

    base_salary: float
    overtime: float = 0.0
    deductions: float = 0.0
    bonuses: float = 0.0

    net_salary: float  # بيتحسب قبل الحفظ

    created_at: datetime = Field(default_factory=datetime.utcnow)
