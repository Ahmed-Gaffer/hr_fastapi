from typing import Optional
from sqlmodel import SQLModel, Field

class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(index=True)
    code: str = Field(index=True)
    name: str
    base_salary: float
    status: str = "نشط"
    department: Optional[str] = None

class EmployeeCreate(SQLModel):
    code: str
    name: str
    base_salary: float
    status: Optional[str] = None
    department: Optional[str] = None

class EmployeeUpdate(SQLModel):
    code: Optional[str] = None
    name: Optional[str] = None
    base_salary: Optional[float] = None
    status: Optional[str] = None
    department: Optional[str] = None
