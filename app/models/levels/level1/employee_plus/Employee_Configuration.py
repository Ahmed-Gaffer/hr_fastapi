# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models/levels/level1/employee++/Employee_Configuration.py
# File Name: Employee_Configuration.py
# -----------------------------------------

from sqlmodel import SQLModel, Field
from typing import Optional

class EmployeeConfiguration(SQLModel, table=True):
    __tablename__ = "employee_configuration"

    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    company_config_id: int = Field(foreign_key="companyconfig.id", index=True)

    custom_value: Optional[str] = None
