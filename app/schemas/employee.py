# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/schemas\employee.py
# File Name: employee.py
# -----------------------------------------

from pydantic import BaseModel
from typing import Optional
from datetime import date


class EmployeeCreate(BaseModel):
    code: str
    name: str
    national_id: Optional[str] = None
    job_title: Optional[str] = None
    hire_date: Optional[date] = None
    base_salary: Optional[float] = 0.0


class EmployeeUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    job_title: Optional[str] = None
    base_salary: Optional[float] = None
    status: Optional[str] = None


class EmployeeRead(BaseModel):
    id: int
    code: str
    name: str
    base_salary: float
    status: str

    class Config:
        orm_mode = True