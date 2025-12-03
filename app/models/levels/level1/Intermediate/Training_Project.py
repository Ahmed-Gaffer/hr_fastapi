from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level1\Intermediate\Training_Project.py
# File Name: Training_Project.py
# -----------------------------------------

class Trainingproject(SQLModel, table=True):
    """جدول وسيط يربط التدريب بالمشروعات (Many-to-Many)"""

    id: Optional[int] = Field(default=None, primary_key=True)
    training_id: int = Field(foreign_key="employeetraining.id", index=True)
    project_id: int = Field(foreign_key="project.id", index=True)

    mandatory: bool = False  # هل التدريب إلزامي للمشروع؟
