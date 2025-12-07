from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level1\units\PerformanceReview.py
# File Name: PerformanceReview.py
# -----------------------------------------

class PerformanceReview(SQLModel, table=True):
    """تقييم الأداء"""
    __tablename__ = "performance_review"
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)

    review_date: date
    reviewer: str
    score: float  # درجة التقييم
    comments: Optional[str] = None