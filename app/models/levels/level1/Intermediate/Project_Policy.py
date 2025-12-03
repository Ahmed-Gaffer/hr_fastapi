# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level1\Intermediate\Project_Policy.py
# File Name: Project_Policy.py
# -----------------------------------------

from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field

class Projectpolicy(SQLModel, table=True):
    """جدول وسيط يربط المشروع بالسياسات"""
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id", index=True)
    policy_id: int = Field(foreign_key="taxpolicy.id", index=True)

    effective_from: Optional[date] = None
    effective_to: Optional[date] = None
