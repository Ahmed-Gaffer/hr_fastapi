# راوتر خاص بإدارة المستخدمين
from fastapi import APIRouter
from sqlmodel import Session, select
from app.database import engine
from app.models.user import User
from app.services.auth import hash_password

# إنشاء الراوتر
router = APIRouter(prefix="/users", tags=["Users"])

# دالة لإضافة مستخدم جديد
@router.post("/", response_model=User)
def create_user(user: User):
    with Session(engine) as session:
        # تشفير كلمة المرور قبل الحفظ
        user.hashed_password = hash_password(user.hashed_password)

        # إضافة المستخدم للجلسة
        session.add(user)

        # حفظ التغييرات
        session.commit()

        # تحديث الكائن بعد الحفظ
        session.refresh(user)

        # إرجاع المستخدم
        return user
