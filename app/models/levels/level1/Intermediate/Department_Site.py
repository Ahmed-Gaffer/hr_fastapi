# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level1\Intermediate\department_site.py
# File Name: department_site.py
# -----------------------------------------


from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level1\Intermediate\Department_site.py
# File Name: Department_site.py
# -----------------------------------------

class DepartmentSite(SQLModel, table=True):
    """جدول وسيط يربط الأقسام بالمواقع (Many-to-Many)"""
    __tablename__ = "department_site"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    department_id: int = Field(foreign_key="department.id", index=True)
    site_id: int = Field(foreign_key="site.id", index=True)

    start_date: Optional[date] = None
    end_date: Optional[date] = None