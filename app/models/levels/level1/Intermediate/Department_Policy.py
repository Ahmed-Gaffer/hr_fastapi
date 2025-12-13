# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level1\Intermediate\department_policy.py
# File Name: department_policy.py
# -----------------------------------------


from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level1\Intermediate\Department_policy.py
# File Name: Department_policy.py
# -----------------------------------------

class DepartmentPolicy(SQLModel, table=True):
    """جدول وسيط يربط الأقسام بالسياسات (Many-to-Many)"""
    __tablename__ = "department_policy"

    id: Optional[int] = Field(default=None, primary_key=True)
    department_id: int = Field(foreign_key="department.id", index=True)
    policy_id: int = Field(foreign_key="tax_policy.id", index=True)

    effective_from: Optional[date] = None
    effective_to: Optional[date] = None