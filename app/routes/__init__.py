from fastapi import APIRouter

from app.routes import (
    attendance,
    auth,
    employees,
    pages,
    reports,
    salary,
    salary_components,
    site,
    system,
    tenants,
    user,
    search,
    analytics,
)
from app.routes.imports import attendance as import_attendance
from app.routes.imports import employees as import_employees
from app.routes.imports import salaries as import_salaries


api_router = APIRouter()

api_router.include_router(tenants.router)
api_router.include_router(employees.router)
api_router.include_router(attendance.router)
api_router.include_router(salary.router)
api_router.include_router(salary_components.router)
api_router.include_router(reports.router)
api_router.include_router(auth.router)
api_router.include_router(site.router)
api_router.include_router(pages.router)
api_router.include_router(system.router)
api_router.include_router(user.router)
api_router.include_router(search.router)
api_router.include_router(analytics.router)

api_router.include_router(import_employees.router, prefix="/imports", tags=["imports"])
api_router.include_router(import_attendance.router, prefix="/imports", tags=["imports"])
api_router.include_router(import_salaries.router, prefix="/imports", tags=["imports"])
