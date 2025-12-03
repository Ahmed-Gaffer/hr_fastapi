# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level2\Employee_Project_CostCenter.py
# File Name: Employee_Project_CostCenter.py
# -----------------------------------------

from typing import Optional
from sqlmodel import SQLModel, Field

class Employeeprojectcostcenter(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالمشروع ومركز التكلفة"""
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    project_id: int = Field(foreign_key="project.id", index=True)
    cost_center_id: int = Field(foreign_key="costcenter.id", index=True)

    allocation_percentage: Optional[float] = None  # نسبة توزيع التكلفة
