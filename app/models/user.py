# تعريف جدول المستخدمين اللي بيسجلوا دخول للنظام
from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # معرف المستخدم
    username: str                                               # اسم المستخدم
    hashed_password: str                                        # كلمة المرور المشفرة
    role: str = "user"                                          # نوع المستخدم (user أو admin)
