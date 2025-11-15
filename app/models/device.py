# تعريف جدول أجهزة البصمة المرتبطة بالمواقع
from sqlmodel import SQLModel, Field
from typing import Optional

# كلاس يمثل جهاز بصمة واحد
class Device(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # معرف الجهاز
    serial_number: str                                          # الرقم التسلسلي للجهاز
    site_id: int = Field(foreign_key="site.id")                 # الموقع المرتبط بالجهاز
    location_hint: Optional[str] = None                         # وصف إضافي لمكان الجهاز (اختياري)
