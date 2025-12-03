# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level2\Employee_Asset_Site.py
# File Name: Employee_Asset_Site.py
# -----------------------------------------

from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field

class Employeeassetsite(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالأصل والموقع"""
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    asset_id: int = Field(foreign_key="asset.id", index=True)
    site_id: int = Field(foreign_key="site.id", index=True)

    assigned_date: Optional[date] = None
    return_date: Optional[date] = None
