# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level1\Intermediate\tenant_department.py
# File Name: tenant_department.py
# -----------------------------------------


from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level1\Intermediate\Tenant_department.py
# File Name: Tenant_department.py
# -----------------------------------------

class TenantDepartment(SQLModel, table=True):
    """جدول وسيط يربط الشركات بالأقسام (Many-to-Many)"""
    __tablename__ = "tenant_department"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(foreign_key="tenant.id", index=True)
    department_id: int = Field(foreign_key="department.id", index=True)