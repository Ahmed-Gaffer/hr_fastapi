class EmployeeBenefit(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالبدلات"""
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    benefit_id: int = Field(foreign_key="benefitrecord.id", index=True)

    amount: Optional[float] = None
    notes: Optional[str] = None
