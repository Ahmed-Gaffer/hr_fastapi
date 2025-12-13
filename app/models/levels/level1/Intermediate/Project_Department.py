# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level1\Intermediate\project_department.py
# File Name: project_department.py
# -----------------------------------------



from typing import Optional
from sqlmodel import SQLModel, Field

class ProjectDepartment(SQLModel, table=True):
    """جدول وسيط يربط المشروع بالأقسام (Many-to-Many)"""
    __tablename__ = "project_department"

    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id", index=True)
    department_id: int = Field(foreign_key="department.id", index=True)

    role: Optional[str] = None  # دور القسم في المشروع
    notes: Optional[str] = None