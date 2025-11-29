from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date


class ProjectSite(SQLModel, table=True):
    """جدول وسيط يربط المشروع بالمواقع (Many-to-Many)"""

    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id", index=True)
    site_id: int = Field(foreign_key="site.id", index=True)

    start_date: Optional[date] = None
    end_date: Optional[date] = None
    notes: Optional[str] = None
