# راوتر خاص بإدارة المواقع
from fastapi import APIRouter
from sqlmodel import Session, select
from app.database import engine
from app.models.site import Site

# إنشاء الراوتر الخاص بالمواقع
router = APIRouter(prefix="/sites", tags=["Sites"])

# دالة لإضافة موقع جديد
@router.post("/", response_model=Site)
def create_site(site: Site):
    with Session(engine) as session:  # فتح جلسة اتصال
        session.add(site)             # إضافة الموقع
        session.commit()              # حفظ التغييرات
        session.refresh(site)         # تحديث الكائن بعد الحفظ
        return site                   # إرجاع الموقع

# دالة لعرض كل المواقع
@router.get("/", response_model=list[Site])
def list_sites():
    with Session(engine) as session:
        return session.exec(select(Site)).all()
