# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level3\employee_training_project_site.py
# File Name: employee_training_project_site.py
# -----------------------------------------



from typing import Optional
from sqlmodel import SQLModel, Field

class EmployeeTrainingProjectSite(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالتدريب والمشروع والموقع"""
    __tablename__ = "employee_training_project_site"

    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    training_id: int = Field(foreign_key="employee_training.id", index=True)
    project_id: int = Field(foreign_key="project.id", index=True)
    site_id: int = Field(foreign_key="site.id", index=True)