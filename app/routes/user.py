# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/routes\user.py
# File Name: user.py
# -----------------------------------------



# راوتر خاص بإدارة المستخدمين
from fastapi import APIRouter
from sqlmodel import Session, select
from app.database import engine
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.auth import hash_password

# إنشاء الراوتر
router = APIRouter(prefix="/users", tags=["Users"])

# دالة لإضافة مستخدم جديد
@router.post("/", response_model=User)
def create_user(user_data: UserCreate):
    with Session(engine) as session:
        # تشفير كلمة المرور
        hashed_password = hash_password(user_data.password)

        # إنشاء كائن المستخدم
        user = User(
            username=user_data.username,
            hashed_password=hashed_password,
            role=user_data.role,
            tenant_id=user_data.tenant_id
        )

        # إضافة المستخدم للجلسة
        session.add(user)

        # حفظ التغييرات
        session.commit()

        # تحديث الكائن بعد الحفظ
        session.refresh(user)

        # إرجاع المستخدم
        return user