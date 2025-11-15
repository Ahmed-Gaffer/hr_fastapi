# تعريف جدول المواقع
from sqlmodel import SQLModel, Field
from typing import Optional

# كلاس يمثل موقع عمل
class Site(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # معرف الموقع
    name: str                                                  # اسم الموقع
    location: Optional[str] = None                             # وصف أو عنوان الموقع
