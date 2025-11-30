from sqlmodel import SQLModel, Field
from typing import Optional

class TenantConfiguration(SQLModel, table=True):
    """جدول وسيط يربط الشركة بالإعدادات"""
    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(foreign_key="tenant.id", index=True)
    config_id: int = Field(foreign_key="configuration.id", index=True)

    value: Optional[str] = None
