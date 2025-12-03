# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models/project.py
# File Name: project.py
# -----------------------------------------

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from sqlalchemy import UniqueConstraint


class Project(SQLModel, table=True):
    """المشروع"""

    __table_args__ = (UniqueConstraint("tenant_id", "name", name="uq_project_tenant_name"),)

    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(foreign_key="tenant.id", index=True)   # الشركة المالكة للمشروع
    site_id: Optional[int] = Field(foreign_key="site.id", index=True)  # الموقع المرتبط بالمشروع

    # 📌 بيانات المشروع
    name: str = Field(index=True)   # اسم المشروع
    code: Optional[str] = Field(default=None, index=True)   # كود المشروع
    description: Optional[str] = None   # وصف إضافي

    # 🔗 علاقات ORM
    tenant: "Tenant" = Relationship(back_populates="projects")
    site: Optional["Site"] = Relationship(back_populates="projects")
    cost_centers: List["CostCenter"] = Relationship(back_populates="project")  # مراكز التكلفة المرتبطة بالمشروع


# 🟢 موديلات Create / Update
class Project(SQLModel):
    tenant_id: int
    site_id: Optional[int] = None
    name: str
    code: Optional[str] = None
    description: Optional[str] = None


class Project(SQLModel):
    tenant_id: Optional[int] = None
    site_id: Optional[int] = None
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
