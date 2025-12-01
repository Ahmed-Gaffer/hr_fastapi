# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level3\Employee_Project_Site_CostCenter.py
# File Name: Employee_Project_Site_CostCenter.py
# -----------------------------------------

from typing import Optional
from sqlmodel import SQLModel, Field

class EmployeeProjectSiteCostCenter(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id")
    project_id: int = Field(foreign_key="project.id")
    site_id: int = Field(foreign_key="site.id")
    cost_center_id: int = Field(foreign_key="costcenter.id")

    allocation_percentage: Optional[float] = None
