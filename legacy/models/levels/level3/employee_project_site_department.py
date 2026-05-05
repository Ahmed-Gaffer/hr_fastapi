# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level3\employee_project_site_department.py
# File Name: employee_project_site_department.py
# -----------------------------------------



from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field

class EmployeeProjectSiteDepartment(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالمشروع والموقع والقسم"""
    __tablename__ = "employee_project_site_department"

    id: Optional[int] = Field(default=None, primary_key=True)

    employee_id: int = Field(foreign_key="employee.id")
    project_id: int = Field(foreign_key="project.id")
    site_id: int = Field(foreign_key="site.id")
    department_id: int = Field(foreign_key="department.id")

    role: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None