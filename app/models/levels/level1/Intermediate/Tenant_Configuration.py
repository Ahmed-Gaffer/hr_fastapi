# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level1\Intermediate\Tenant_Configuration.py
# File Name: Tenant_Configuration.py
# -----------------------------------------

from sqlmodel import SQLModel, Field
from typing import Optional

class TenantConfiguration(SQLModel, table=True):
    __tablename__ = "tenant_configuration"

    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(foreign_key="tenant.id", index=True)
    company_config_id: int = Field(foreign_key="companyconfig.id", index=True)

    custom_value: Optional[str] = None
