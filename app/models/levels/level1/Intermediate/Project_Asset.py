from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level1\Intermediate\Project_Asset.py
# File Name: Project_Asset.py
# -----------------------------------------

class Project_Asset(SQLModel, table=True):
    """جدول وسيط يربط المشروعات بالأصول (Many-to-Many)"""
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id", index=True)
    asset_id: int = Field(foreign_key="asset.id", index=True)

    assigned_date: Optional[date] = None
    return_date: Optional[date] = None