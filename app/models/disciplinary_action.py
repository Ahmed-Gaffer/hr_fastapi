from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\models\levels\level1\units\DisciplinaryAction.py
# File Name: DisciplinaryAction.py
# -----------------------------------------

class DisciplinaryAction(SQLModel, table=True):
    """العقوبات والجزاءات"""
    __tablename__ = "disciplinary_action"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)

    action_type: str  # خصم، إنذار، فصل
    action_date: date
    description: Optional[str] = None
    approved_by: Optional[str] = None
