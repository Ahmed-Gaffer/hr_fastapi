# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level3\employee_asset_project_site.py
# File Name: employee_asset_project_site.py
# -----------------------------------------



# File Path: app/models/levels/level3/employee_asset_project_site.py
# File Name: employee_asset_project_site.py
# -----------------------------------------

from sqlmodel import SQLModel, Field
from typing import Optional


class EmployeeAssetProjectSite(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالأصل والمشروع والموقع (Many-to-Many)"""
    __tablename__ = "employee_asset_project_site"

    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    asset_id: int = Field(foreign_key="asset.id", index=True)
    project_id: int = Field(foreign_key="project.id", index=True)
    site_id: int = Field(foreign_key="site.id", index=True)