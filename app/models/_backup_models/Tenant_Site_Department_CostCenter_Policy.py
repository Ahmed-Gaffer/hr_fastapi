# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level4\Tenant_Site_Department_CostCenter_Policy.py
# File Name: Tenant_Site_Department_CostCenter_Policy.py
# -----------------------------------------

from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field

class Tenant_Site_Department_CostCenter_Policy(SQLModel, table=True):
    """جدول وسيط يربط الشركة بالموقع والقسم ومركز التكلفة والسياسة"""
    id: Optional[int] = Field(default=None, primary_key=True)

    tenant_id: int = Field(foreign_key="tenant.id")
    site_id: int = Field(foreign_key="site.id")
    department_id: int = Field(foreign_key="department.id")
    cost_center_id: int = Field(foreign_key="costcenter.id")
    policy_id: int = Field(foreign_key="taxpolicy.id")

    effective_from: Optional[date] = None
    effective_to: Optional[date] = None
