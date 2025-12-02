from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level1\Intermediate\Tenant_Site.py
# File Name: Tenant_Site.py
# -----------------------------------------

class Tenant_Site(SQLModel, table=True):
    """جدول وسيط يربط الشركات بالمواقع (Many-to-Many)"""
    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(foreign_key="tenant.id", index=True)
    site_id: int = Field(foreign_key="site.id", index=True)