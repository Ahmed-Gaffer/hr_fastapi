# راوتر خاص بالحضور
from fastapi import APIRouter
from sqlmodel import Session, select
from app.database import engine
from app.models.attendance import Attendance
from app.models.employee import Employee
from fastapi.responses import HTMLResponse  # ← استيراد نوع الاستجابة HTML

# إنشاء الراوتر
router = APIRouter(prefix="/attendance", tags=["Attendance"])

# دالة لإضافة سجل حضور
@router.post("/", response_model=Attendance)
def check_in(att: Attendance):
    with Session(engine) as session:  # فتح جلسة اتصال بقاعدة البيانات
        session.add(att)              # إضافة السجل
        session.commit()              # حفظ التغييرات
        session.refresh(att)          # تحديث الكائن بعد الحفظ
        return att                    # إرجاع السجل

# دالة لعرض كل سجلات الحضور
@router.get("/", response_model=list[Attendance])
def list_attendance():
    with Session(engine) as session:
        return session.exec(select(Attendance)).all()


# إنشاء الراوتر
router = APIRouter(prefix="/attendance", tags=["Attendance"])

# دالة تعرض الحضور كـ HTML (لـ HTMX)
@router.get("/list", response_class=HTMLResponse)
def list_attendance_htmx():
    with Session(engine) as session:
        records = session.exec(select(Attendance)).all()  # جلب كل سجلات الحضور

        # بناء HTML بسيط لعرضهم
        html = "<ul class='space-y-2'>"

        for record in records:
            # عرض اسم الموظف وتاريخ الحضور ووقت الدخول والخروج
            html += f"<li class='p-2 border rounded bg-gray-50'>📅 {record.date} - 👤 موظف رقم {record.employee_id} - دخول: {record.check_in} - خروج: {record.check_out}</li>"

        html += "</ul>"
        return html