# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level2\Employee_Department_Site.py
# File Name: Employee_Department_Site.py
# -----------------------------------------

# File Path: app/models/levels/level2/Employee_Department_Site.py
# File Name: Employee_Department_Site.py
# -----------------------------------------

from sqlmodel import SQLModel, Field
from typing import Optional


class Employee_Department_Site(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالقسم والموقع (Many-to-Many)"""

    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    department_id: int = Field(foreign_key="department.id", index=True)
    site_id: int = Field(foreign_key="site.id", index=True)
