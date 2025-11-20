from sqlmodel import SQLModel, Field
from typing import Optional

class EmployeeDetails(SQLModel, table=True):
    """تفاصيل إضافية للموظف (حالة اجتماعية، عنوان، إلخ)"""
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", index=True, unique=True)
    
    # 👥 الحالة الاجتماعية والعائلة
    marital_status: str = "أعزب"  # أعزب، متزوج، مطلق
    spouse_name: Optional[str] = None
    spouse_works: bool = False  # هل الزوجة تعمل؟
    num_children: int = 0
    
    # 📍 العنوان والتأمين
    governorate: str = "القاهرة"  # المحافظة
    city: Optional[str] = None
    address: Optional[str] = None
    
    # 🏥 التأمين
    has_comprehensive_insurance: bool = False  # هل يستحق التأمين الشامل (حسب المحافظة)
    
    notes: Optional[str] = None