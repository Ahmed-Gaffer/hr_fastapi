# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level2\employee_policy_cost_center.py
# File Name: employee_policy_cost_center.py
# -----------------------------------------



from typing import Optional
from sqlmodel import SQLModel, Field

class EmployeePolicyCostCenter(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالسياسة ومركز التكلفة"""
    __tablename__ = "employee_policy_cost_center"

    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    policy_id: int = Field(foreign_key="tax_policy.id", index=True)
    cost_center_id: int = Field(foreign_key="cost_center.id", index=True)

    effective_from: Optional[date] = None
    effective_to: Optional[date] = None