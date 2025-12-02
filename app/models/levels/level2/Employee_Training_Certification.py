# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level2\Employee_Training_Certification.py
# File Name: Employee_Training_Certification.py
# -----------------------------------------

from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field

class Employee_Training_Certification(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالتدريب والشهادة"""
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    training_id: int = Field(foreign_key="employeetraining.id", index=True)
    certification_id: int = Field(foreign_key="employeecertification.id", index=True)

    certificate_date: Optional[date] = None
