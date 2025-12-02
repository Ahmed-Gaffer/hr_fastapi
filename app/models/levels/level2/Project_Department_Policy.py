# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level2\Project_Department_Policy.py
# File Name: Project_Department_Policy.py
# -----------------------------------------

from sqlmodel import SQLModel, Field
from typing import Optional

class Project_Department_Policy(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    department_id: int = Field(foreign_key="department.id")
    policy_id: int = Field(foreign_key="taxpolicy.id")
