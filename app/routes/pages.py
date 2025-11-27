import os
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(tags=["pages"])

# ✅ مسار index (SPA)
BUILD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "build"))
INDEX_HTML = os.path.join(BUILD_DIR, "index.html")

@router.get("/", response_class=FileResponse)
def serve_index():
    if os.path.exists(INDEX_HTML):
        return FileResponse(INDEX_HTML)
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
