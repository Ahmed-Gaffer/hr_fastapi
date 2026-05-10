# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level1\Intermediate\tenant_policy.py
# File Name: tenant_policy.py
# -----------------------------------------


from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level1\Intermediate\Tenant_policy.py
# File Name: Tenant_policy.py
# -----------------------------------------

class TenantPolicy(SQLModel, table=True):
    """جدول وسيط يربط الشركة بالسياسات (Many-to-Many)"""
    __tablename__ = "tenant_policy"

    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(foreign_key="tenant.id", index=True)
    policy_id: int = Field(foreign_key="tax_policy.id", index=True)

    effective_from: Optional[date] = None
    effective_to: Optional[date] = None