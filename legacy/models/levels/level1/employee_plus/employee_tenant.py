# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level1\employee_plus\employee_tenant.py
# File Name: employee_tenant.py
# -----------------------------------------



from typing import Optional
from sqlmodel import SQLModel, Field

class EmployeeTenant(SQLModel, table=True):
    """جدول وسيط يربط الشركة بالموظفين"""
    __tablename__ = "employee_tenant"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(foreign_key="tenant.id", index=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)

    contract_type: Optional[str] = None  # دائم، مؤقت، خارجي