# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models/levels/level1/employee++/Employee_BenefitRecord.py
# File Name: Employee_BenefitRecord.py
# -----------------------------------------

class EmployeeBenefit(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالبدلات"""
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    benefit_id: int = Field(foreign_key="benefitrecord.id", index=True)

    amount: Optional[float] = None
    notes: Optional[str] = None
