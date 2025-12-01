# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level3\Employee_Training_Certification_Project.py
# File Name: Employee_Training_Certification_Project.py
# -----------------------------------------

from typing import Optional
from sqlmodel import SQLModel, Field

class EmployeeTrainingCertificationProject(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id")
    training_id: int = Field(foreign_key="employeetraining.id")
    certification_id: int = Field(foreign_key="employeecertification.id")
    project_id: int = Field(foreign_key="project.id")
