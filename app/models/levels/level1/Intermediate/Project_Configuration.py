# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level1\Intermediate\Project_Configuration.py
# File Name: Project_Configuration.py
# -----------------------------------------

from sqlmodel import SQLModel, Field
from typing import Optional

class ProjectConfiguration(SQLModel, table=True):
    """جدول وسيط يربط المشروع بالإعدادات"""
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id", index=True)
    config_id: int = Field(foreign_key="configuration.id", index=True)

    value: Optional[str] = None
