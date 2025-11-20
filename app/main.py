from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_db_and_tables
from app.routes.employee import router as employee_router
from app.routes.site import router as site_router
from app.routes.attendance import router as attendance_router
from app.routes.user import router as user_router
from app.routes.auth import router as auth_router
from app.routes.imports import router as imports_router
from app.routes.pages import router as pages_router

app = FastAPI(title="HR System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_db_and_tables()

app.include_router(employee_router)  # تأكد السطر ده موجود
print("Included routers: employees")
app.include_router(site_router)
app.include_router(attendance_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(imports_router)
app.include_router(pages_router)