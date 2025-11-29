from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from sqlalchemy import UniqueConstraint


class Site(SQLModel, table=True):
    """الموقع"""

    __table_args__ = (UniqueConstraint("tenant_id", "name", name="uq_site_tenant_name"),)

    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(foreign_key="tenant.id", index=True)  # الشركة المالكة للموقع
    name: str = Field(index=True)  # اسم الموقع
    location: Optional[str] = None  # العنوان أو الموقع الجغرافي

    # 🔗 علاقات ORM
    tenant: "Tenant" = Relationship(back_populates="sites")
    employees: List["Employee"] = Relationship(back_populates="site")
    projects: List["Project"] = Relationship(back_populates="site")


# 🟢 موديلات Create / Update
class SiteCreate(SQLModel):
    tenant_id: int
    name: str
    location: Optional[str] = None


class SiteUpdate(SQLModel):
    tenant_id: Optional[int] = None
    name: Optional[str] = None
    location: Optional[str] = None
