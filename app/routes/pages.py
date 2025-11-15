from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

# مسار "/" يرجع صفحة index.html مباشرة
@router.get("/", response_class=FileResponse)
def serve_index():
    return FileResponse("frontend/index.html")

# مسارات صفحات HTML الأخرى
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
