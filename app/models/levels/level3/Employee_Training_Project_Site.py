# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level3\Employee_Training_Project_Site.py
# File Name: Employee_Training_Project_Site.py
# -----------------------------------------

from typing import Optional
from sqlmodel import SQLModel, Field

class Employeetrainingprojectsite(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالتدريب والمشروع والموقع"""
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    training_id: int = Field(foreign_key="employeetraining.id", index=True)
    project_id: int = Field(foreign_key="project.id", index=True)
    site_id: int = Field(foreign_key="site.id", index=True)
