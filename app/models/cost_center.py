# app/models/cost_center.py
from sqlmodel import SQLModel, Field
from typing import Optional

class CostCenter(SQLModel, table=True):
    """مركز التكلفة"""
    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(foreign_key="tenant.id", index=True)
    name: str
    code: str = Field(index=True)
