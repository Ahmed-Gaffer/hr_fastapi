from typing import Optional
from sqlmodel import SQLModel, Field

class ProjectCostCenter(SQLModel, table=True):
    """جدول وسيط يربط المشروع بمراكز التكلفة"""
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id", index=True)
    cost_center_id: int = Field(foreign_key="costcenter.id", index=True)

    budget_allocation: Optional[float] = None
