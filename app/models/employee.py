# تعريف جدول الموظفين
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

# كلاس يمثل جدول الموظف
class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # مفتاح داخلي للجدول
    employee_id: str = Field(default_factory=lambda: str(uuid.uuid4()), unique=True, index=True)  # يولّده النظام تلقائيًا
    national_id: Optional[str] = Field(default=None, unique=True, index=True)  # الرقم القومي (لو موجود)
    legacy_code: Optional[str] = Field(default=None, unique=True, index=True)  # الكود القديم (لو موجود)

    full_name: str
    title: Optional[str] = None
    phone: Optional[str] = None
    status: str = Field(default="active")
    hire_date: Optional[datetime] = None

    site_name: Optional[str] = None
    company_name: Optional[str] = None
    cost_center: Optional[str] = None
    insured: bool = Field(default=False)
    overnight: bool = Field(default=False)

    site_id: Optional[int] = Field(default=None, foreign_key="site.id")