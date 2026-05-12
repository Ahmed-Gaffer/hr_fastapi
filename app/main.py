# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/main.py
# File Name: main.py
# -----------------------------------------

# app/main.py

import os
import logging
import traceback
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import PlainTextResponse

from app.routes import api_router
from app.database import create_db_and_tables

# 🔥 Logging واضح في التيرمنال
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s | %(name)s | %(message)s",
)

app = FastAPI(title="نظام إدارة الموارد البشرية")

app.include_router(api_router, prefix="/api")

BUILD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "build"))
STATIC_DIR = os.path.join(BUILD_DIR, "static")
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 أي Exception هيتطبع كامل في التيرمنال
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print("\n🔥🔥🔥 UNHANDLED EXCEPTION 🔥🔥🔥")
    traceback.print_exc()
    return PlainTextResponse(
        "Internal Server Error — check terminal logs",
        status_code=500,
    )

@app.on_event("startup")
def on_startup():
    print("Starting application...")
    create_db_and_tables()   # ❌ ممنوع try/except هنا
