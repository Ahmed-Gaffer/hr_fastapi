# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level2\Employee_Policy_CostCenter.py
# File Name: Employee_Policy_CostCenter.py
# -----------------------------------------

from typing import Optional
from sqlmodel import SQLModel, Field

class Employeepolicycostcenter(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالسياسة ومركز التكلفة"""
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    policy_id: int = Field(foreign_key="taxpolicy.id", index=True)
    cost_center_id: int = Field(foreign_key="costcenter.id", index=True)

    effective_from: Optional[date] = None
    effective_to: Optional[date] = None
