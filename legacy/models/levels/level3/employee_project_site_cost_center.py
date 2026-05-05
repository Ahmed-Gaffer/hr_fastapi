# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level3\employee_project_site_cost_center.py
# File Name: employee_project_site_cost_center.py
# -----------------------------------------



from typing import Optional
from sqlmodel import SQLModel, Field

class EmployeeProjectSiteCostCenter(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالمشروع والموقع ومركز التكلفة"""
    __tablename__ = "employee_project_site_cost_center"

    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id")
    project_id: int = Field(foreign_key="project.id")
    site_id: int = Field(foreign_key="site.id")
    cost_center_id: int = Field(foreign_key="cost_center.id")

    allocation_percentage: Optional[float] = None