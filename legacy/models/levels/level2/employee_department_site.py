# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level2\employee_department_site.py
# File Name: employee_department_site.py
# -----------------------------------------



# File Path: app/models/levels/level2/employee_department_site.py
# File Name: employee_department_site.py
# -----------------------------------------

from sqlmodel import SQLModel, Field
from typing import Optional


class EmployeeDepartmentSite(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالقسم والموقع (Many-to-Many)"""
    __tablename__ = "employee_department_site"

    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    department_id: int = Field(foreign_key="department.id", index=True)
    site_id: int = Field(foreign_key="site.id", index=True)