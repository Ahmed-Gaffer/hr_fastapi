# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/database.py
# File Name: database.py
# -----------------------------------------

from typing import Generator
from sqlmodel import SQLModel, create_engine, Session
import os

# حاول الحصول على DATABASE_uRL من إعدادات المشروع، عدّل إذا مسارك مختلف
try:
    from app.core.config import DATABASE_uRL
except Exception:
    DATABASE_uRL = os.environ.get("DATABASE_uRL", "sqlite:///./dev.db")

engine = create_engine(DATABASE_uRL, echo=True)

def create_db_and_tables() -> None:
    """Create tables from SQLModel metadata."""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()