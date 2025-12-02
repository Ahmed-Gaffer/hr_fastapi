# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models/levels/level1/employee++/Employee_Tenant.py
# File Name: Employee_Tenant.py
# -----------------------------------------

from typing import Optional
from sqlmodel import SQLModel, Field

class Employee_Tenant(SQLModel, table=True):
    """جدول وسيط يربط الشركة بالموظفين"""
    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(foreign_key="tenant.id", index=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)

    contract_type: Optional[str] = None  # دائم، مؤقت، خارجي
