# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level1\employee_plus\employee_configuration.py
# File Name: employee_configuration.py
# -----------------------------------------



from sqlmodel import SQLModel, Field
from typing import Optional

class EmployeeConfiguration(SQLModel, table=True):
    __tablename__ = "employee_configuration"

    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    company_config_id: int = Field(foreign_key="company_config.id", index=True)

    custom_value: Optional[str] = None