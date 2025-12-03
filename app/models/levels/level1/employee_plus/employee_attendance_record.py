# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models/levels/level1/employee++/Employee_AttendanceRecord.py
# File Name: Employee_AttendanceRecord.py
# -----------------------------------------

from sqlmodel import SQLModel, Field
from typing import Optional

class Employeeattendancerecord(SQLModel, table=True):
    """جدول وسيط يربط الموظف بسجلات الحضور"""
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    attendance_id: int = Field(foreign_key="attendancerecord.id", index=True)

    status: Optional[str] = None  # حاضر، غائب، متأخر
