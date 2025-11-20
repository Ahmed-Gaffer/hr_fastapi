# تعريف جدول الموظفين
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, datetime

class Employee(SQLModel, table=True):
    """الموظف (مع Tenant)"""
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # ⭐ Multi-tenancy
    tenant_id: int = Field(foreign_key="tenant.id", index=True)
    
    # معلومات أساسية
    code: str = Field(index=True)  # كود الموظف (فريد ضمن الشركة)
    name: str
    role: Optional[str] = None
    department: Optional[str] = None
    
    # معلومات التعاقد
    site_id: Optional[int] = Field(foreign_key="site.id")
    cost_center_id: Optional[int] = Field(foreign_key="costcenter.id")
    hire_date: Optional[date] = None
    contract_type: str = "دائم"  # دائم، مؤقت، موسمي
    
    # معلومات شخصية
    national_id: Optional[str] = Field(index=True)
    insurance_number: Optional[str] = Field(index=True)
    phone: Optional[str] = None
    email: Optional[str] = None
    
    # معلومات مالية
    base_salary: float = 0
    status: str = "نشط"  # نشط، معطل، منتهي
    
    # التتبع
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    __table_args__ = (
        {"indexes": [
            "tenant_id, code",  # فريد ضمن الشركة
        ]},
    )