# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level3\employee_project_role_cost_center.py
# File Name: employee_project_role_cost_center.py
# -----------------------------------------



from typing import Optional
from sqlmodel import SQLModel, Field

class EmployeeProjectRoleCostCenter(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالمشروع والدور ومركز التكلفة"""
    __tablename__ = "employee_project_role_cost_center"

    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    project_id: int = Field(foreign_key="project.id", index=True)
    role_id: int = Field(foreign_key="employee_role.id", index=True)
    cost_center_id: int = Field(foreign_key="cost_center.id", index=True)

    allocation_percentage: Optional[float] = None