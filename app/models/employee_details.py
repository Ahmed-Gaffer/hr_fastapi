from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


class EmployeeDetails(SQLModel, table=True):
    """تفاصيل إضافية للموظف (حالة اجتماعية، عنوان، إلخ)"""
    id: Optional[int] = Field(default=None, primary_key=True)

    # 🔗 علاقة أساسية مع الموظف (1:1)
    employee_id: int = Field(foreign_key="employee.id", index=True, unique=True)

    # 👥 الحالة الاجتماعية والعائلة
    marital_status: str = "أعزب"   # أعزب، متزوج، مطلق
    spouse_name: Optional[str] = None
    spouse_works: bool = False     # هل الزوج/الزوجة يعمل؟
    num_children: int = 0

    # 📍 العنوان والتأمين
    governorate: str = "القاهرة"   # المحافظة
    city: Optional[str] = None
    address: Optional[str] = None

    # 🏥 التأمين
    has_comprehensive_insurance: bool = False   # هل يستحق التأمين الشامل (حسب المحافظة)
    notes: Optional[str] = None

    # 🔗 علاقة ORM
    employee: "Employee" = Relationship(back_populates="details")


# 🟢 موديلات Create / Update
class EmployeeDetailsCreate(SQLModel):
    employee_id: int
    marital_status: Optional[str] = None
    spouse_name: Optional[str] = None
    spouse_works: Optional[bool] = None
    num_children: Optional[int] = None
    governorate: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    has_comprehensive_insurance: Optional[bool] = None
    notes: Optional[str] = None


class EmployeeDetailsUpdate(SQLModel):
    marital_status: Optional[str] = None
    spouse_name: Optional[str] = None
    spouse_works: Optional[bool] = None
    num_children: Optional[int] = None
    governorate: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    has_comprehensive_insurance: Optional[bool] = None
    notes: Optional[str] = None
