# تعريف جدول المرتبات الشهرية
from sqlmodel import SQLModel, Field
from typing import Optional

# كلاس يمثل سجل مرتب لموظف في شهر معين
class SalaryRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # معرف السجل
    employee_id: int = Field(foreign_key="employee.id")        # معرف الموظف
    month: str                                                 # الشهر بصيغة "2025-11"
    base_salary: float                                         # المرتب الأساسي
    days_present: int                                          # عدد أيام الحضور
    deductions: float                                          # الخصومات
    net_salary: float                                          # المرتب النهائي بعد الخصم
