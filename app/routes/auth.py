# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\routes\auth.py
# File Name: auth.py
# -----------------------------------------

# استيراد الأدوات المطلوبة من FastAPI
from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse

# استيراد أدوات التعامل مع قاعدة البيانات
from sqlmodel import Session, select
from app.database import engine

# استيراد نموذج المستخدم ودوال التوثيق
from app.models.user import User
from app.services.auth import verify_password, create_access_token

# إنشاء راوتر خاص بالتوثيق
router = APIRouter(prefix="/auth", tags=["Authentication"])

# دالة تسجيل الدخول باستخدام بيانات النموذج (Form)
@router.post("/login", response_class=HTMLResponse)
def login(username: str = Form(...), password: str = Form(...)):
    # فتح جلسة اتصال بقاعدة البيانات
    with Session(engine) as session:
        # البحث عن المستخدم حسب اسم المستخدم
        user = session.exec(select(User).where(User.username == username)).first()

        # التحقق من وجود المستخدم وصحة كلمة المرور
        if not user or not verify_password(password, user.hashed_password):
            # لو البيانات غلط، نرجّع رسالة خطأ بلون أحمر
            return "<span style='color:red'>بيانات الدخول غير صحيحة</span>"

        # إنشاء توكن JWT يحتوي على اسم المستخدم والصلاحية
        token = create_access_token({"sub": user.username, "role": user.role})

        # إرجاع التوكن داخل صفحة HTML
        return f"<span>توكن الدخول: <br><code>{token}</code></span>"
