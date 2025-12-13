# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level3\employee_training_certification_project.py
# File Name: employee_training_certification_project.py
# -----------------------------------------



from typing import Optional
from sqlmodel import SQLModel, Field

class EmployeeTrainingCertificationProject(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالتدريب والشهادة والمشروع"""
    __tablename__ = "employee_training_certification_project"

    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id")
    training_id: int = Field(foreign_key="employee_training.id")
    certification_id: int = Field(foreign_key="employee_certification.id")
    project_id: int = Field(foreign_key="project.id")