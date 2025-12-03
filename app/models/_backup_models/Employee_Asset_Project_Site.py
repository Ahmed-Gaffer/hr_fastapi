# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level3\Employee_Asset_Project_Site.py
# File Name: Employee_Asset_Project_Site.py
# -----------------------------------------

# File Path: app/models/levels/level3/Employee_Asset_Project_Site.py
# File Name: Employee_Asset_Project_Site.py
# -----------------------------------------

from sqlmodel import SQLModel, Field
from typing import Optional


class EmployeeAssetProjectSite(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالأصل والمشروع والموقع (Many-to-Many)"""

    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    asset_id: int = Field(foreign_key="asset.id", index=True)
    project_id: int = Field(foreign_key="project.id", index=True)
    site_id: int = Field(foreign_key="site.id", index=True)
