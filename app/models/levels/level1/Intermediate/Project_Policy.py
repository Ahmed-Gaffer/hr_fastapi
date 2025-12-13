# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level1\Intermediate\project_policy.py
# File Name: project_policy.py
# -----------------------------------------



from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field

class ProjectPolicy(SQLModel, table=True):
    """جدول وسيط يربط المشروع بالسياسات"""
    __tablename__ = "project_policy"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id", index=True)
    policy_id: int = Field(foreign_key="tax_policy.id", index=True)

    effective_from: Optional[date] = None
    effective_to: Optional[date] = None