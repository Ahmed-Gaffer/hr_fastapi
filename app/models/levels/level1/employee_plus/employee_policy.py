# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models/levels/level1/employee++/employee_policy.py
# File Name: employee_policy.py
# -----------------------------------------

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date


class Employeepolicy(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالسياسات الضريبية (Many-to-Many)"""

    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    tax_policy_id: int = Field(foreign_key="taxpolicy.id", index=True)

    # 📌 بيانات إضافية عن العلاقة
    effective_from: Optional[date] = None  # تاريخ بداية تطبيق السياسة على الموظف
    effective_to: Optional[date] = None    # تاريخ نهاية تطبيق السياسة (لو مؤقتة)
    notes: Optional[str] = None            # ملاحظات إضافية
