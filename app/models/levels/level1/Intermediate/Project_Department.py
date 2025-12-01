# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level1\Intermediate\Project_Department.py
# File Name: Project_Department.py
# -----------------------------------------

from typing import Optional
from sqlmodel import SQLModel, Field

class ProjectDepartment(SQLModel, table=True):
    """جدول وسيط يربط المشروع بالأقسام (Many-to-Many)"""

    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id", index=True)
    department_id: int = Field(foreign_key="department.id", index=True)

    role: Optional[str] = None  # دور القسم في المشروع
    notes: Optional[str] = None
