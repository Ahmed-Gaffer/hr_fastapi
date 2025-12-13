# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level4\employee_training_certification_project_site.py
# File Name: employee_training_certification_project_site.py
# -----------------------------------------



from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field

class EmployeeTrainingCertificationProjectSite(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالتدريب والشهادة والمشروع والموقع"""
    __tablename__ = "employee_training_certification_project_site"

    id: Optional[int] = Field(default=None, primary_key=True)

    employee_id: int = Field(foreign_key="employee.id")
    training_id: int = Field(foreign_key="employee_training.id")
    certification_id: int = Field(foreign_key="employee_certification.id")
    project_id: int = Field(foreign_key="project.id")
    site_id: int = Field(foreign_key="site.id")

    certificate_date: Optional[date] = None