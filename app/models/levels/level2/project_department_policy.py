# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level2\project_department_policy.py
# File Name: project_department_policy.py
# -----------------------------------------



from sqlmodel import SQLModel, Field
from typing import Optional

class ProjectDepartmentPolicy(SQLModel, table=True):
    """جدول وسيط يربط المشروع بالقسم والسياسة"""
    __tablename__ = "project_department_policy"

    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    department_id: int = Field(foreign_key="department.id")
    policy_id: int = Field(foreign_key="tax_policy.id")