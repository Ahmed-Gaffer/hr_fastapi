from fastapi import FastAPI
from app.routes import tenants, employees, imports
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="نظام الرواتب الذكي - Nageeah HR")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# الراوترات
app.include_router(tenants.router)
app.include_router(employees.router)
app.include_router(imports.router)

@app.get("/")
async def root():
    return {
        "system": "نظام الرواتب الذكي",
        "company": "نجيده للمقاولات",
        "version": "1.0.0",
        "status": "ready"
    }