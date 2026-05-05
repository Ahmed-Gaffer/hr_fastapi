# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level1\Intermediate\project_configuration.py
# File Name: project_configuration.py
# -----------------------------------------



from sqlmodel import SQLModel, Field
from typing import Optional

class ProjectConfiguration(SQLModel, table=True):
    """جدول وسيط يربط المشروعات بإعدادات الشركة"""
    __tablename__ = "project_configuration"

    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id", index=True)
    company_config_id: int = Field(foreign_key="company_config.id", index=True)

    custom_value: Optional[str] = None