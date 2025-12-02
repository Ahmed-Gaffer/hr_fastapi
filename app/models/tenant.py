# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models/tenant.py
# File Name: tenant.py
# -----------------------------------------

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum

from app.models.project import Project


class TenantStatus(str, Enum):
    ACTIVE = "نشط"
    INACTIVE = "معطل"
    TRIAL = "تجريبي"
    EXPIRED = "منتهي"


class Tenant(SQLModel, table=True):
    """المؤسسة / الشركة (Tenant)"""

    id: Optional[int] = Field(default=None, primary_key=True)

    # 🏢 معلومات الشركة
    name: str
    code: Optional[str] = Field(default=None, unique=True)
    legal_name: Optional[str] = None
    industry: str = "مقاولات"

    # 📍 العنوان
    address: Optional[str] = None
    city: Optional[str] = None
    governorate: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    tax_id: Optional[str] = None

    # 📌 الحالة والاشتراك
    status: TenantStatus = TenantStatus.ACTIVE
    subscription_type: str = "premium"
    subscription_start: datetime = Field(default_factory=datetime.utcnow)
    subscription_end: Optional[datetime] = None

    # 👤 المعلومات الإدارية
    owner_name: Optional[str] = None
    owner_phone: Optional[str] = None
    owner_email: Optional[str] = None

    # 🕒 تتبع
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_default: bool = False

    # 🔗 علاقات ORM
    employees: List["Employee"] = Relationship(back_populates="tenant")
    sites: List["Site"] = Relationship(back_populates="tenant")
    projects: List["Project"] = Relationship(back_populates="tenant")
    departments: List["Department"] = Relationship(back_populates="tenant")
    cost_centers: List["CostCenter"] = Relationship(back_populates="tenant")
    salaries: List["SalaryRecord"] = Relationship(back_populates="tenant")
    attendances: List["Attendance"] = Relationship(back_populates="tenant")


# 🟢 موديلات Create / Update
class TenantCreate(SQLModel):
    name: str
    code: Optional[str] = None
    legal_name: Optional[str] = None
    industry: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    governorate: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    tax_id: Optional[str] = None
    status: Optional[TenantStatus] = None
    subscription_type: Optional[str] = None
    subscription_end: Optional[datetime] = None
    owner_name: Optional[str] = None
    owner_phone: Optional[str] = None
    owner_email: Optional[str] = None


class TenantUpdate(SQLModel):
    name: Optional[str] = None
    code: Optional[str] = None
    legal_name: Optional[str] = None
    industry: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    governorate: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    tax_id: Optional[str] = None
    status: Optional[TenantStatus] = None
    subscription_type: Optional[str] = None
    subscription_end: Optional[datetime] = None
    owner_name: Optional[str] = None
    owner_phone: Optional[str] = None
    owner_email: Optional[str] = None
