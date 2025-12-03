# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level4\Employee_Training_Certification_Project_Site.py
# File Name: Employee_Training_Certification_Project_Site.py
# -----------------------------------------

from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field

class Employeetrainingcertificationprojectsite(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالتدريب والشهادة والمشروع والموقع"""
    id: Optional[int] = Field(default=None, primary_key=True)

    employee_id: int = Field(foreign_key="employee.id")
    training_id: int = Field(foreign_key="employeetraining.id")
    certification_id: int = Field(foreign_key="employeecertification.id")
    project_id: int = Field(foreign_key="project.id")
    site_id: int = Field(foreign_key="site.id")

    certificate_date: Optional[date] = None
