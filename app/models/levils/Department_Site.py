class DepartmentSite(SQLModel, table=True):
    """جدول وسيط يربط الأقسام بالمواقع (Many-to-Many)"""
    id: Optional[int] = Field(default=None, primary_key=True)
    department_id: int = Field(foreign_key="department.id", index=True)
    site_id: int = Field(foreign_key="site.id", index=True)

    start_date: Optional[date] = None
    end_date: Optional[date] = None