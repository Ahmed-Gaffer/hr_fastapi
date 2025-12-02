# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level1\Intermediate\Tenant_Configuration.py
# File Name: Tenant_Configuration.py
# -----------------------------------------

from sqlmodel import SQLModel, Field
from typing import Optional

class Tenant_Configuration(SQLModel, table=True):
    """جدول وسيط يربط الشركة بالإعدادات"""
    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(foreign_key="tenant.id", index=True)
    config_id: int = Field(foreign_key="configuration.id", index=True)

    value: Optional[str] = None
