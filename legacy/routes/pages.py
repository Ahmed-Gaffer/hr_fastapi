# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/routes\pages.py
# File Name: pages.py
# -----------------------------------------



import os
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(tags=["pages"])

# ✅ مسار index (SPA)
BUILD_dIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "build"))
INDEX_hTML = os.path.join(BUILD_dIR, "index.html")

@router.get("/", response_class=FileResponse)
def serve_index():
    if os.path.exists(INDEX_hTML):
        return FileResponse(INDEX_hTML)
    return {"detail": "Frontend build not found."}

# ✅ صفحات HTML الأخرى
@router.get("/employees_view.html", response_class=FileResponse)
def serve_employees_view():
    return FileResponse("frontend/employees_view.html")

@router.get("/employee_add.html", response_class=FileResponse)
def serve_employee_add():
    return FileResponse("frontend/employee_add.html")

@router.get("/attendance_view.html", response_class=FileResponse)
def serve_attendance_view():
    return FileResponse("frontend/attendance_view.html")

@router.get("/login_htmx.html", response_class=FileResponse)
def serve_login_htmx():
    return FileResponse("frontend/login_htmx.html")