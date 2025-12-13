# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level2\employee_project_site.py
# File Name: employee_project_site.py
# -----------------------------------------



from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field

class EmployeeProjectSite(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالمشروع والموقع"""
    __tablename__ = "employee_project_site"

    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    project_id: int = Field(foreign_key="project.id", index=True)
    site_id: int = Field(foreign_key="site.id", index=True)

    start_date: Optional[date] = None
    end_date: Optional[date] = None
    role: Optional[str] = None