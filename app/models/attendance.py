from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import date, time


class Attendance(SQLModel, table=True):
    """سجل حضور الموظف"""

    id: Optional[int] = Field(default=None, primary_key=True)

    # 🔗 علاقات أساسية
    employee_id: int = Field(foreign_key="employee.id", index=True)
    site_id: Optional[int] = Field(foreign_key="site.id", index=True)

    # 🕒 بيانات الحضور
    date: date
    check_in: Optional[time] = None
    check_out: Optional[time] = None
    status: str = "حاضر"  # حاضر، غائب، متأخر

    # 🔗 علاقة ORM
    employee: "Employee" = Relationship(back_populates="attendances")
    site: Optional["Site"] = Relationship()  # لو عايز تربط الحضور بالموقع مباشرة


# 🟢 موديلات Create / Update
class AttendanceCreate(SQLModel):
    employee_id: int
    site_id: Optional[int] = None
    date: date
    check_in: Optional[time] = None
    check_out: Optional[time] = None


class AttendanceUpdate(SQLModel):
    employee_id: Optional[int] = None
    site_id: Optional[int] = None
    date: Optional[date] = None
    check_in: Optional[time] = None
    check_out: Optional[time] = None
