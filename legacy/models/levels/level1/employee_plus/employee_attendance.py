# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level1\employee_plus\employee_attendance.py
# File Name: employee_attendance.py
# -----------------------------------------



from sqlmodel import SQLModel, Field
from typing import Optional

class EmployeeAttendance(SQLModel, table=True):
    """جدول وسيط يربط الموظف بسجلات الحضور"""
    __tablename__ = "employee_attendance"
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    attendance_id: int = Field(foreign_key="attendance.id", index=True)

    status: Optional[str] = None  # حاضر، غائب، متأخر