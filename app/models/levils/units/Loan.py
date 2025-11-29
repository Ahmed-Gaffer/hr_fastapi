class Loan(SQLModel, table=True):
    """قروض الموظفين"""
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)

    principal_amount: float  # أصل القرض
    interest_rate: float = 0.0
    start_date: date
    end_date: Optional[date] = None
    monthly_installment: float
    notes: Optional[str] = None