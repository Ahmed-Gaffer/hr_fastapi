class ProjectAsset(SQLModel, table=True):
    """جدول وسيط يربط المشروعات بالأصول (Many-to-Many)"""
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id", index=True)
    asset_id: int = Field(foreign_key="asset.id", index=True)

    assigned_date: Optional[date] = None
    return_date: Optional[date] = None