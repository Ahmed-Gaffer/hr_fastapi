# app/models/site.py
from sqlmodel import SQLModel, Field
from typing import Optional

# جدول المواقع
class Site(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)   # معرف الموقع
    name: str = Field(index=True, unique=True)                  # اسم الموقع (مميز وفريد)
    location: Optional[str] = None                              # وصف أو عنوان الموقع
    company_name: Optional[str] = None                          # اسم الشركة التابعة
    cost_center: Optional[str] = None                           # مركز التكلفة
