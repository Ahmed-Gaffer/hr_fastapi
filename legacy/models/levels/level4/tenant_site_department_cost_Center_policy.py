# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level4\tenant_site_department_cost_Center_policy.py
# File Name: tenant_site_department_cost_Center_policy.py
# -----------------------------------------



from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field

class TenantSiteDepartmentCostCenterPolicy(SQLModel, table=True):
    """جدول وسيط يربط الشركة بالموقع والقسم ومركز التكلفة والسياسة"""
    __tablename__ = "tenant_site_department_cost_center_policy"

    id: Optional[int] = Field(default=None, primary_key=True)

    tenant_id: int = Field(foreign_key="tenant.id")
    site_id: int = Field(foreign_key="site.id")
    department_id: int = Field(foreign_key="department.id")
    cost_center_id: int = Field(foreign_key="cost_center.id")
    policy_id: int = Field(foreign_key="tax_policy.id")

    effective_from: Optional[date] = None
    effective_to: Optional[date] = None