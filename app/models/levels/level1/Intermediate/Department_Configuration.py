# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level1\Intermediate\Department_Configuration.py
# File Name: Department_Configuration.py
# -----------------------------------------

from typing import Optional
from sqlmodel import SQLModel, Field

class Department_Configuration(SQLModel, table=True):
    """جدول وسيط يربط القسم بالإعدادات"""
    id: Optional[int] = Field(default=None, primary_key=True)
    department_id: int = Field(foreign_key="department.id", index=True)
    config_id: int = Field(foreign_key="configuration.id", index=True)

    value: Optional[str] = None
