from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from app.database import create_db_and_tables
from app.services.import_excel import import_employees_from_excel

# استيراد الراوترات
from app.routes.employee import router as employee_router
from app.routes.site import router as site_router
from app.routes.attendance import router as attendance_router
from app.routes.user import router as user_router
from app.routes.auth import router as auth_router
from app.routes.imports import router as imports_router
from app.routes.pages import router as pages_router

app = FastAPI(title="HR System")

create_db_and_tables()

# ربط الراوترات
app.include_router(employee_router)
app.include_router(site_router)
app.include_router(attendance_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(imports_router)
app.include_router(pages_router)

# ربط مجلد frontend كـ static files على "/static"
app.mount("/static", StaticFiles(directory="frontend", html=True), name="static")