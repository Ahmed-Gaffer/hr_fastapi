# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level1\Intermediate\project_site.py
# File Name: project_site.py
# -----------------------------------------

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date


class Project_Site(SQLModel, table=True):
    """جدول وسيط يربط المشروع بالمواقع (Many-to-Many)"""

    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id", index=True)
    site_id: int = Field(foreign_key="site.id", index=True)

    start_date: Optional[date] = None
    end_date: Optional[date] = None
    notes: Optional[str] = None
