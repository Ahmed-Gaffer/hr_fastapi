# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level3\tenant_site_department_cost_center.py
# File Name: tenant_site_department_cost_center.py
# -----------------------------------------



from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import date

class TenantSiteDepartmentCostCenter(SQLModel, table=True):
    """جدول وسيط يربط الشركة بالموقع والقسم ومركز التكلفة"""
    __tablename__ = "tenant_site_department_cost_center"

    id: Optional[int] = Field(default=None, primary_key=True)

    tenant_id: int = Field(foreign_key="tenant.id", index=True)
    site_id: int = Field(foreign_key="site.id", index=True)
    department_id: int = Field(foreign_key="department.id", index=True)
    cost_center_id: int = Field(foreign_key="cost_center.id", index=True)

    allocation_percentage: Optional[float] = None  # نسبة توزيع التكلفة
    effective_from: Optional[date] = None
    effective_to: Optional[date] = None