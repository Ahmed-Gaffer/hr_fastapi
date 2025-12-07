# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level1\Intermediate\Department_Configuration.py
# File Name: Department_Configuration.py
# -----------------------------------------

from typing import Optional
from sqlmodel import SQLModel, Field

class DepartmentConfiguration(SQLModel, table=True):
    __tablename__ = "department_configuration"

    id: Optional[int] = Field(default=None, primary_key=True)
    department_id: int = Field(foreign_key="department.id", index=True)
    company_config_id: int = Field(foreign_key="companyconfig.id", index=True)

    custom_value: Optional[str] = None
