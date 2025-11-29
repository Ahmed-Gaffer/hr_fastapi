class ProjectDepartment(SQLModel, table=True):
    """جدول وسيط يربط المشروع بالأقسام (Many-to-Many)"""

    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id", index=True)
    department_id: int = Field(foreign_key="department.id", index=True)

    role: Optional[str] = None  # دور القسم في المشروع
    notes: Optional[str] = None
