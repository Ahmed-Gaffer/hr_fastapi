class DepartmentPolicy(SQLModel, table=True):
    """جدول وسيط يربط الأقسام بالسياسات (Many-to-Many)"""
    id: Optional[int] = Field(default=None, primary_key=True)
    department_id: int = Field(foreign_key="department.id", index=True)
    policy_id: int = Field(foreign_key="taxpolicy.id", index=True)

    effective_from: Optional[date] = None
    effective_to: Optional[date] = None