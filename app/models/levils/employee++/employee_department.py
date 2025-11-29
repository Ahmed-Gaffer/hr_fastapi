from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date


class EmployeeDepartment(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالأقسام (Many-to-Many)"""

    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    department_id: int = Field(foreign_key="department.id", index=True)

    # 📌 بيانات إضافية عن العلاقة
    role: Optional[str] = None  # دور الموظف في القسم (مثلاً: رئيس قسم، عضو فريق)
    start_date: Optional[date] = None  # تاريخ بداية الانضمام للقسم
    end_date: Optional[date] = None    # تاريخ نهاية الانضمام (لو انتقل لقسم آخر)
