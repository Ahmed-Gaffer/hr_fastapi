from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class Site(SQLModel, table=True):
    """الموقع"""
    id: Optional[int] = Field(default=None, primary_key=True)

    tenant_id: int = Field(foreign_key="tenant.id", index=True)
    name: str = Field(index=True, unique=True)
    location: Optional[str] = None
    company_name: Optional[str] = None
    cost_center: Optional[str] = None

    # 🔗 علاقات ORM
    tenant: "Tenant" = Relationship(back_populates="sites")
    employees: List["Employee"] = Relationship(back_populates="site")
    projects: List["Project"] = Relationship(back_populates="site")


class SiteCreate(SQLModel):
    tenant_id: int
    name: str
    location: Optional[str] = None
    company_name: Optional[str] = None
    cost_center: Optional[str] = None


class SiteUpdate(SQLModel):
    tenant_id: Optional[int] = None
    name: Optional[str] = None
    location: Optional[str] = None
    company_name: Optional[str] = None
    cost_center: Optional[str] = None
