# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level1\Intermediate\training_project.py
# File Name: training_project.py
# -----------------------------------------


from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level1\Intermediate\Training_project.py
# File Name: Training_project.py
# -----------------------------------------

class TrainingProject(SQLModel, table=True):
    """جدول وسيط يربط التدريب بالمشروعات (Many-to-Many)"""
    __tablename__ = "training_project"

    id: Optional[int] = Field(default=None, primary_key=True)
    training_id: int = Field(foreign_key="employee_training.id", index=True)
    project_id: int = Field(foreign_key="project.id", index=True)

    mandatory: bool = False  # هل التدريب إلزامي للمشروع؟