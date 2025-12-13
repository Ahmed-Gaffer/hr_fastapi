# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\levels\level1\employee_plus\employee_training.py
# File Name: employee_training.py
# -----------------------------------------



from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import date

class EmployeeTraining(SQLModel, table=True):
    """جدول وسيط يربط الموظف بالدورات التدريبية والشهادات"""
    __tablename__ = "employee_training"

    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)

    # 📚 بيانات التدريب
    training_name: str  # اسم الدورة أو التدريب
    provider: Optional[str] = None  # الجهة المقدمة (مثلاً: مركز تدريب، جامعة، شركة)
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    # 🎓 بيانات الشهادة
    certificate_received: bool = False
    certificate_name: Optional[str] = None
    certificate_date: Optional[date] = None

    # 📌 ملاحظات إضافية
    notes: Optional[str] = None

    # 🔗 علاقات ORM
    employee: "Employee" = Relationship(back_populates="trainings")