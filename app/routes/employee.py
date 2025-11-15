# راوتر خاص بالموظفين
from fastapi import APIRouter, Form, Depends                    # استيراد الأدوات المطلوبة من FastAPI
from fastapi.responses import HTMLResponse                      # استيراد نوع الاستجابة HTML
from sqlmodel import Session, select                            # أدوات التعامل مع قاعدة البيانات
from app.database import engine                                 # الاتصال بقاعدة البيانات
from app.models.employee import Employee                        # نموذج الموظف
from app.dependencies.auth_guard import require_admin           # التحقق من صلاحية المدير

# إنشاء الراوتر الخاص بالموظفين
router = APIRouter(prefix="/employees", tags=["Employees"])

# دالة لإضافة موظف جديد من HTMX
@router.post("/add", response_class=HTMLResponse)
def add_employee_htmx(
    full_name: str = Form(...),                                 # الاسم الكامل من النموذج
    title: str = Form(None),                                    # المسمى الوظيفي (اختياري)
    phone: str = Form(None),                                    # رقم الهاتف (اختياري)
    status: str = Form("active"),                               # الحالة (افتراضي "active")
    user=Depends(require_admin)                                 # التحقق من أن المستخدم مدير
):
    with Session(engine) as session:                            # فتح جلسة اتصال بقاعدة البيانات
        emp = Employee(                                         # إنشاء كائن موظف جديد
            full_name=full_name,
            title=title,
            phone=phone,
            status=status
        )
        session.add(emp)                                        # إضافة الموظف للجلسة
        session.commit()                                        # حفظ التغييرات في قاعدة البيانات
        session.refresh(emp)                                    # تحديث الكائن بعد الحفظ
        return f"<span style='color:green'>تم إضافة الموظف: {emp.full_name}</span>"  # إرجاع رسالة نجاح


# دالة تعرض كل الموظفين كـ HTML (لـ HTMX)
@router.get("/list", response_class=HTMLResponse)
def list_employees_htmx():
    with Session(engine) as session:
        employees = session.exec(select(Employee)).all()  # جلب كل الموظفين

        # بناء HTML بسيط لعرضهم
        html = "<ul class='space-y-2'>"

        for emp in employees:
            html += f"<li class='p-2 border rounded bg-gray-50'>👤 {emp.full_name} - {emp.title or 'بدون مسمى'}</li>"

        html += "</ul>"
        return html