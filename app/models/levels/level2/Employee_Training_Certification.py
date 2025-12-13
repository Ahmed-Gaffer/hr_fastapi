# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level2\employee_training_certification.py
# File Name: employee_training_certification.py
# -----------------------------------------



from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field

class EmployeeTrainingCertification(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالتدريب والشهادة"""

    __tablename__ = "employee_training_certification"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    training_id: int = Field(foreign_key="employee_training.id", index=True)
    certification_id: int = Field(foreign_key="employee_certification.id", index=True)

    certificate_date: Optional[date] = None