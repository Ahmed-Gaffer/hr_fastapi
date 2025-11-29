class AssetSite(SQLModel, table=True):
    """جدول وسيط يربط الأصل بالمواقع (Many-to-Many)"""

    id: Optional[int] = Field(default=None, primary_key=True)
    asset_id: int = Field(foreign_key="asset.id", index=True)
    site_id: int = Field(foreign_key="site.id", index=True)

    assigned_date: Optional[date] = None
    return_date: Optional[date] = None
    notes: Optional[str] = None
