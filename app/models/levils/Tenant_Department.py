class TenantDepartment(SQLModel, table=True):
    """جدول وسيط يربط الشركات بالأقسام (Many-to-Many)"""
    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(foreign_key="tenant.id", index=True)
    department_id: int = Field(foreign_key="department.id", index=True)