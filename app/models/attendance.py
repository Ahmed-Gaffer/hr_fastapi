from typing import Optional
from datetime import date, time, datetime
from sqlmodel import SQLModel, Field


class Attendance(SQLModel, table=True):
    __tablename__ = "attendance"

    id: Optional[int] = Field(default=None, primary_key=True)

    tenant_id: int = Field(index=True)
    employee_id: int = Field(index=True)

    date: date
    check_in: Optional[time] = None
    check_out: Optional[time] = None

    status: str = Field(default="present")  # present | absent | late
    shift: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
