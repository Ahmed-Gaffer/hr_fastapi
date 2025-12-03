from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level1\Intermediate\Tenant_Department.py
# File Name: Tenant_Department.py
# -----------------------------------------

class Tenantdepartment(SQLModel, table=True):
    """جدول وسيط يربط الشركات بالأقسام (Many-to-Many)"""
    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(foreign_key="tenant.id", index=True)
    department_id: int = Field(foreign_key="department.id", index=True)