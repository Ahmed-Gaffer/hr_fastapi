# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\scripts\test_attendance.py
# File Name: test_attendance.py
# -----------------------------------------

# سكريبت بسيط لتسجيل حضور موظف يدويًا (للاختبار فقط)

from sqlmodel import Session
from datetime import date, time
from app.database import engine
from app.models.attendance import Attendance

# فتح جلسة اتصال بقاعدة البيانات
with Session(engine) as session:
    # إنشاء سجل حضور جديد
    att = Attendance(
        employee_id=1,             # رقم الموظف
        site_id=1,                 # رقم الموقع
        date=date.today(),         # تاريخ اليوم
        check_in=time(8, 30),      # وقت الدخول
        check_out=time(17, 0)      # وقت الخروج
    )

    # إضافة السجل للجلسة
    session.add(att)

    # حفظ التغييرات
    session.commit()

    # طباعة تأكيد
    print("تم تسجيل الحضور بنجاح")
