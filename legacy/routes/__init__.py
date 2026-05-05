# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/routes\__init__.py
# File Name: __init__.py
# -----------------------------------------



from fastapi import APIRouter

# ✅ الراوترات الأساسية
from app.routes import tenants, employees, attendance, salary, reports, auth, site, pages, system

# ✅ الاستيراد من ملفات imports
from app.routes.imports import employees as import_employees
from app.routes.imports import attendance as import_attendance
from app.routes.imports import salaries as import_salaries

api_router = APIRouter()

# ✅ الراوترات الأساسية
api_router.include_router(tenants.router)
api_router.include_router(employees.router)
api_router.include_router(attendance.router)
api_router.include_router(salary.router)   # CRUD للرواتب
api_router.include_router(reports.router)
api_router.include_router(auth.router)
api_router.include_router(site.router)
api_router.include_router(pages.router)   # صفحات HTML تحت قسم pages
api_router.include_router(system.router)  # نظام وصحة النظام

# ✅ الاستيراد كله تحت قسم واحد imports
api_router.include_router(import_employees.router, prefix="/imports", tags=["imports"])
api_router.include_router(import_attendance.router, prefix="/imports", tags=["imports"])
api_router.include_router(import_salaries.router, prefix="/imports", tags=["imports"])