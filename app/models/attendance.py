# تعريف جدول الحضور
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, time

# كلاس يمثل سجل حضور لموظف
class Attendance(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # معرف الحضور
    employee_id: int = Field(foreign_key="employee.id")        # معرف الموظف
    site_id: Optional[int] = Field(default=None, foreign_key="site.id")  # معرف الموقع
    date: date                                                 # تاريخ الحضور
    check_in: Optional[time] = None                            # وقت الدخول
    check_out: Optional[time] = None                           # وقت الخروج
