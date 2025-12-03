# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level4\Employee_Asset_Project_Site_Role.py
# File Name: Employee_Asset_Project_Site_Role.py
# -----------------------------------------

from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field

class Employeeassetprojectsiterole(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالأصل والمشروع والموقع والدور"""
    id: Optional[int] = Field(default=None, primary_key=True)

    employee_id: int = Field(foreign_key="employee.id")
    asset_id: int = Field(foreign_key="asset.id")
    project_id: int = Field(foreign_key="project.id")
    site_id: int = Field(foreign_key="site.id")
    role_id: int = Field(foreign_key="employeerole.id")

    assigned_date: Optional[date] = None
    return_date: Optional[date] = None
