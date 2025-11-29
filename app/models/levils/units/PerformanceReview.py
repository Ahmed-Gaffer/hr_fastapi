class PerformanceReview(SQLModel, table=True):
    """تقييم الأداء"""
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)

    review_date: date
    reviewer: str
    score: float  # درجة التقييم
    comments: Optional[str] = None