# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level3\Employee_Asset_Site_Role.py
# File Name: Employee_Asset_Site_Role.py
# -----------------------------------------

from typing import Optional
from sqlmodel import SQLModel, Field

class EmployeeAssetSiteRole(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id")
    asset_id: int = Field(foreign_key="asset.id")
    site_id: int = Field(foreign_key="site.id")
    role_id: int = Field(foreign_key="employeerole.id")
