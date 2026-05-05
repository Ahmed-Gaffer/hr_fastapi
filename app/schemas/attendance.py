from pydantic import BaseModel
from typing import Optional
from datetime import date, time


class AttendanceCreate(BaseModel):
    employee_id: int
    date: date
    check_in: Optional[time] = None
    check_out: Optional[time] = None
    status: Optional[str] = "present"
    shift: Optional[str] = None


class AttendanceRead(BaseModel):
    id: int
    employee_id: int
    date: date
    check_in: Optional[time]
    check_out: Optional[time]
    status: str
    shift: Optional[str]

    class Config:
        orm_mode = True
