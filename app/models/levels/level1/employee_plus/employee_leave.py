# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level1\employee_plus\employee_leave.py
# File Name: employee_leave.py
# -----------------------------------------



from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date
from enum import Enum


class LeaveType(str, Enum):
    """أنواع الإجازات"""
    ANNUAL = "سنوية"
    SICK = "مرضية"
    EMERGENCY = "طارئة"
    UNPAID = "بدون مرتب"
    OTHER = "أخرى"


class employee_leave(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالإجازات (Many-to-Many)"""

    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)

    leave_type: LeaveType
    start_date: date
    end_date: date

    # 📌 بيانات إضافية
    approved_by: Optional[str] = None  # اسم المدير اللي وافق
    notes: Optional[str] = None