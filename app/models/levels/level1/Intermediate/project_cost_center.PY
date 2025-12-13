from typing import Optional
from sqlmodel import SQLModel, Field

class ProjectCostCenter(SQLModel, table=True):
    """جدول وسيط يربط المشروع بمراكز التكلفة"""
    __tablename__ = "project_cost_center"
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id", index=True)
    cost_center_id: int = Field(foreign_key="cost_center.id", index=True)

    budget_allocation: Optional[float] = None
