# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level2\project_employee_role.py
# File Name: project_employee_role.py
# -----------------------------------------




from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field

class ProjectEmployeeRole(SQLModel, table=True):
    """جدول وسيط يربط المشروع بالموظف والدور"""
    __tablename__ = "project_employee_role"

    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id", index=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    role_id: int = Field(foreign_key="employee_role.id", index=True)

    start_date: Optional[date] = None
    end_date: Optional[date] = None