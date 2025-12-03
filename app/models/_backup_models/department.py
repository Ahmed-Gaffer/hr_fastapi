# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models/department.py
# File Name: department.py
# -----------------------------------------

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from sqlalchemy import UniqueConstraint


class Department(SQLModel, table=True):
    """جدول الأقسام"""

    __table_args__ = (UniqueConstraint("tenant_id", "name", name="uq_department_tenant_name"),)

    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(foreign_key="tenant.id", index=True)  # الشركة المالكة للقسم
    name: str = Field(index=True)  # اسم القسم
    description: Optional[str] = None  # وصف إضافي

    # 🔗 علاقة ORM مع الموظفين
    employees: List["Employee"] = Relationship(back_populates="department")

    # 🔗 علاقة ORM مع الشركة
    tenant: "Tenant" = Relationship(back_populates="departments")


# 🟢 موديلات Create / Update
class Department(SQLModel):
    tenant_id: int
    name: str
    description: Optional[str] = None


class Department(SQLModel):
    tenant_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
