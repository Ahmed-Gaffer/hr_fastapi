# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level1\Intermediate\department_configuration.py
# File Name: department_configuration.py
# -----------------------------------------



from typing import Optional
from sqlmodel import SQLModel, Field

class DepartmentConfiguration(SQLModel, table=True):
    __tablename__ = "department_configuration"

    id: Optional[int] = Field(default=None, primary_key=True)
    department_id: int = Field(foreign_key="department.id", index=True)
    company_config_id: int = Field(foreign_key="company_config.id", index=True)

    custom_value: Optional[str] = None