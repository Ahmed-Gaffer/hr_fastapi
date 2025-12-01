# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/main.py
# File Name: main.py
# -----------------------------------------

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes import api_router
from app.database import create_db_and_tables

app = FastAPI(title="HR FastAPI")

# ✅ كل الـ APIs تحت /api
app.include_router(api_router, prefix="/api")

# ✅ Serve static files من الـ frontend لو موجود
BUILD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "build"))
STATIC_DIR = os.path.join(BUILD_DIR, "static")
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ✅ إعدادات CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    try:
        create_db_and_tables()
    except Exception:
        pass