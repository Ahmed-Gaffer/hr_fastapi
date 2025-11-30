from sqlmodel import SQLModel, Field
from typing import Optional

class EmployeeConfiguration(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالإعدادات"""
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    config_id: int = Field(foreign_key="configuration.id", index=True)

    value: Optional[str] = None
