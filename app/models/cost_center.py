# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models/cost_center.py
# File Name: cost_center.py
# -----------------------------------------

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from sqlalchemy import UniqueConstraint

from app.models.salary import SalaryRecord



class CostCenter(SQLModel, table=True):
    """مركز التكلفة"""

    __table_args__ = (UniqueConstraint("project_id", "name", name="uq_costcenter_project_name"),)

    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id", index=True)
    tenant_id: int = Field(foreign_key="tenant.id", index=True)
    site_id: Optional[int] = Field(foreign_key="site.id", index=True)

    name: str = Field(index=True)
    code: Optional[str] = None
    description: Optional[str] = None

    # علاقات ORM
    project: "Project" = Relationship(back_populates="cost_centers")
    tenant: "Tenant" = Relationship(back_populates="cost_centers")
    site: Optional["Site"] = Relationship(back_populates="cost_centers")
    employees: List["Employee"] = Relationship(back_populates="cost_center")
    salaries: List["SalaryRecord"] = Relationship(back_populates="cost_center")


# 🟢 موديلات Create / Update
class CostCenterCreate(SQLModel):
    project_id: int
    name: str
    code: Optional[str] = None
    description: Optional[str] = None


class CostCenterUpdate(SQLModel):
    project_id: Optional[int] = None
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
