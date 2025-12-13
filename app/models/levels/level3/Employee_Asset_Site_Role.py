# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level3\employee_asset_site_role.py
# File Name: employee_asset_site_role.py
# -----------------------------------------



from typing import Optional
from sqlmodel import SQLModel, Field

class EmployeeAssetSiteRole(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالأصل والموقع والدور"""
    __tablename__ = "employee_asset_site_role"

    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id")
    asset_id: int = Field(foreign_key="asset.id")
    site_id: int = Field(foreign_key="site.id")
    role_id: int = Field(foreign_key="employee_role.id")