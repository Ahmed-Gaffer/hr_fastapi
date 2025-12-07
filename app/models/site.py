# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models/site.py
# File Name: site.py
# -----------------------------------------

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from sqlalchemy import UniqueConstraint

from app.models.tenant import Tenant
from app.models.employee import Employee
from app.models.project import Project
from app.models.cost_center import CostCenter
from app.models.attendance import Attendance


class Site(SQLModel, table=True):
    """الموقع"""
    __tablename__ = "site"

    __table_args__ = (
        UniqueConstraint("tenant_id", "name", name="uq_site_tenant_name"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)

    tenant_id: int = Field(
        foreign_key="tenant.id",
        index=True
    )

    name: str = Field(index=True)
    location: Optional[str] = None

    # 🔗 علاقات ORM
    tenant: Tenant = Relationship(back_populates="sites")

    employees: List[Employee] = Relationship(back_populates="site")
    projects: List[Project] = Relationship(back_populates="site")
    cost_centers: List[CostCenter] = Relationship(back_populates="site")
    attendances: List[Attendance] = Relationship(back_populates="site")


# 🟢 موديلات Create / Update
class SiteCreate(SQLModel):
    tenant_id: int
    name: str
    location: Optional[str] = None


class SiteUpdate(SQLModel):
    tenant_id: Optional[int] = None
    name: Optional[str] = None
    location: Optional[str] = None
