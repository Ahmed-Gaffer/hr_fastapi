from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from sqlalchemy import UniqueConstraint


class Project(SQLModel, table=True):
    """المشروع / مركز التكلفة"""

    __table_args__ = (UniqueConstraint("tenant_id", "name", name="uq_project_tenant_name"),)

    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(foreign_key="tenant.id", index=True)   # الشركة المالكة للمشروع
    site_id: Optional[int] = Field(foreign_key="site.id", index=True)  # الموقع المرتبط بالمشروع

    # 📌 بيانات المشروع
    name: str = Field(index=True)   # اسم المشروع / مركز التكلفة
    code: Optional[str] = Field(default=None, index=True)   # كود المشروع
    description: Optional[str] = None   # وصف إضافي

    # 🔗 علاقات ORM
    tenant: "Tenant" = Relationship(back_populates="projects")
    site: Optional["Site"] = Relationship(back_populates="projects")
    employees: List["Employee"] = Relationship(back_populates="project")
    salaries: List["SalaryRecord"] = Relationship(back_populates="project")


# 🟢 موديلات Create / Update
class ProjectCreate(SQLModel):
    tenant_id: int
    site_id: Optional[int] = None
    name: str
    code: Optional[str] = None
    description: Optional[str] = None


class ProjectUpdate(SQLModel):
    tenant_id: Optional[int] = None
    site_id: Optional[int] = None
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
