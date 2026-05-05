# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level1\employee_plus\employee_public_holiday.py
# File Name: employee_public_holiday.py
# -----------------------------------------



from sqlmodel import SQLModel, Field
from typing import Optional

class EmployeePublicHoliday(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالإجازات الرسمية"""
    __tablename__ = "employee_public_holiday"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    holiday_id: int = Field(foreign_key="public_holiday.id", index=True)

    is_paid: bool = True
    notes: Optional[str] = None