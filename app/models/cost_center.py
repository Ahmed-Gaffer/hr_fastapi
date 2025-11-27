from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class Project(SQLModel, table=True):
    """المشروع / مركز التكلفة"""
    id: Optional[int] = Field(default=None, primary_key=True)

    tenant_id: int = Field(foreign_key="tenant.id", index=True)   # الشركة
    site_id: Optional[int] = Field(foreign_key="site.id", index=True)  # الموقع

    # 📌 بيانات المشروع / مركز التكلفة
    name: str = Field(index=True)       # اسم المشروع / مركز التكلفة
    code: Optional[str] = Field(default=None, index=True)  # كود المشروع / مركز التكلفة
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
