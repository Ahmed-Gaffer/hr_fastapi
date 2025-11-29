class DisciplinaryAction(SQLModel, table=True):
    """العقوبات والجزاءات"""
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)

    action_type: str  # خصم، إنذار، فصل
    action_date: date
    description: Optional[str] = None
    approved_by: Optional[str] = None
