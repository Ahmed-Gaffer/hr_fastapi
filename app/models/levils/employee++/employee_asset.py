from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date


class EmployeeAsset(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالأصول أو المعدات (Many-to-Many)"""

    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)

    asset_name: str  # اسم الأصل أو المعدة (مثلاً: لابتوب، خوذة، سيارة)
    assigned_date: Optional[date] = None
    return_date: Optional[date] = None
    notes: Optional[str] = None
