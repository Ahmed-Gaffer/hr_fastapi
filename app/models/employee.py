# تعريف جدول الموظفين
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

# كلاس يمثل جدول الموظف
class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # معرف الموظف
    legacy_code: Optional[str] = None                          # كود الموظف القديم
    full_name: str                                             # الاسم الكامل
    title: Optional[str] = None                                # المسمى الوظيفي
    phone: Optional[str] = None                                # رقم الهاتف
    status: str = "active"                                     # الحالة (افتراضي active)
    hire_date: Optional[datetime] = None                       # تاريخ التعيين

    site_name: Optional[str] = None                            # اسم الموقع
    company_name: Optional[str] = None                         # اسم الشركة
    cost_center: Optional[str] = None                          # مركز التكلفة
    insured: Optional[bool] = False                            # هل مؤمن عليه
    overnight: Optional[bool] = False                          # هل يبيت في الموقع

    site_id: Optional[int] = Field(default=None, foreign_key="site.id")  # الموقع المرتبط بالموظف
