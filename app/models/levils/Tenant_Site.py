class TenantSite(SQLModel, table=True):
    """جدول وسيط يربط الشركات بالمواقع (Many-to-Many)"""
    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(foreign_key="tenant.id", index=True)
    site_id: int = Field(foreign_key="site.id", index=True)