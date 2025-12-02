# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models/levels/level1/employee++/employee_project.py
# File Name: employee_project.py
# -----------------------------------------

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date


class Employee_Project(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالمشروعات (Many-to-Many)"""

    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    project_id: int = Field(foreign_key="project.id", index=True)

    # 📌 بيانات إضافية عن العلاقة
    role: Optional[str] = None  # دور الموظف في المشروع (مهندس، مشرف، عامل...)
    start_date: Optional[date] = None  # تاريخ بداية العمل في المشروع
    end_date: Optional[date] = None    # تاريخ نهاية العمل في المشروع (لو انتهى)
