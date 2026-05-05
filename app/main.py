from fastapi import FastAPI
from app.database import create_db_and_tables

from app.routes.employees import router as employees_router
from app.routes.attendance import router as attendance_router
from app.routes.salaries import router as salaries_router

app = FastAPI(title="HR System")

# ربط الروتز
app.include_router(employees_router, prefix="/api")
app.include_router(attendance_router, prefix="/api")
app.include_router(salaries_router, prefix="/api")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
