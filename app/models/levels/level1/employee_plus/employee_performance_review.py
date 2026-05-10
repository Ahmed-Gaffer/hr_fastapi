# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level1\employee_plus\employee_performance_review.py
# File Name: employee_performance_review.py
# -----------------------------------------



from sqlmodel import SQLModel, Field
from typing import Optional

class EmployeePerformanceReview(SQLModel, table=True):
    """جدول وسيط يربط الموظف بتقييمات الأداء"""
    __tablename__ = "employee_performance_review"
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    review_id: int = Field(foreign_key="performance_review.id", index=True)

    final_score: Optional[float] = None