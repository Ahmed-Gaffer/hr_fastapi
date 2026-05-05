# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\employee.py
# File Name: employee.py
# -----------------------------------------

from typing import Optional
from datetime import datetime, date
from sqlmodel import SQLModel, Field


class Employee(SQLModel, table=True):
    __tablename__ = "employees"

    id: Optional[int] = Field(default=None, primary_key=True)

    # multi-tenant
    tenant_id: int = Field(index=True)

    # basic info
    code: str = Field(index=True)
    name: str

    national_id: Optional[str] = Field(default=None, index=True)
    job_title: Optional[str] = None
    hire_date: Optional[date] = None

    base_salary: float = 0.0
    status: str = Field(default="active")  # active | suspended | terminated

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)