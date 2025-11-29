class TenantPolicy(SQLModel, table=True):
    """جدول وسيط يربط الشركة بالسياسات (Many-to-Many)"""

    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(foreign_key="tenant.id", index=True)
    policy_id: int = Field(foreign_key="taxpolicy.id", index=True)

    effective_from: Optional[date] = None
    effective_to: Optional[date] = None
