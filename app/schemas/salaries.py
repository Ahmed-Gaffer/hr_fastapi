from pydantic import BaseModel
from datetime import date
from typing import Optional


class SalaryCreate(BaseModel):
    employee_id: int
    month: date
    overtime: Optional[float] = 0.0
    deductions: Optional[float] = 0.0
    bonuses: Optional[float] = 0.0


class SalaryRead(BaseModel):
    id: int
    employee_id: int
    month: date
    base_salary: float
    overtime: float
    deductions: float
    bonuses: float
    net_salary: float

    class Config:
        orm_mode = True
