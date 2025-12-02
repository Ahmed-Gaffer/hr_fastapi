# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models/levels/level1/employee++/employee_skill.py
# File Name: employee_skill.py
# -----------------------------------------

from sqlmodel import SQLModel, Field
from typing import Optional


class Employee_Skill(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالمهارات (Many-to-Many)"""

    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    skill_name: str  # اسم المهارة (مثلاً: إدارة مشاريع، AutoCAD، محاسبة)
    skill_level: Optional[str] = None  # مستوى المهارة (مبتدئ، متوسط، خبير)
