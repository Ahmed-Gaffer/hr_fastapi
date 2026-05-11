# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\user.py
# File Name: user.py
# -----------------------------------------



from sqlmodel import SQLModel, Field
from typing import Optional


class User(SQLModel, table=True):
    """جدول المستخدمين اللي بيسجلوا دخول للنظام"""

    id: Optional[int] = Field(default=None, primary_key=True)  # معرف المستخدم
    username: str  # اسم المستخدم
    hashed_password: str  # كلمة المرور المشفرة
    role: str = "user"  # نوع المستخدم (user أو admin)
    tenant_id: int = Field(default=1)  # معرف الشركة