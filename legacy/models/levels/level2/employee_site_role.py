# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level2\employee_site_role.py
# File Name: employee_site_role.py
# -----------------------------------------



from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class EmployeeSiteRole(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالموقع والدور"""
    __tablename__ = "employee_site_role"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    site_id: int = Field(foreign_key="site.id", index=True)
    role_id: int = Field(foreign_key="employee_role.id", index=True)

    start_date: Optional[date] = None
    end_date: Optional[date] = None