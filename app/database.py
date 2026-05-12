# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/database.py
# File Name: database.py
# -----------------------------------------

from typing import Generator
from sqlmodel import SQLModel, create_engine, Session
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "hr.db"))

# حاول الحصول على DATABASE_URL من إعدادات المشروع، عدّل إذا مسارك مختلف
try:
    from app.core.config import DATABASE_URL
except Exception:
    DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH}")

if not DATABASE_URL:
    DATABASE_URL = f"sqlite:///{DEFAULT_DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False},
)

def create_db_and_tables() -> None:
    """Create tables from SQLModel metadata."""
    SQLModel.metadata.create_all(engine)
    _populate_default_tenant_and_user()


def _populate_default_tenant_and_user() -> None:
    """Ensure there is a default tenant and admin user for quick access."""
    from sqlmodel import select
    from app.models.tenant import Tenant, TenantStatus
    from app.models.company_config import CompanyConfig
    from app.models.user import User
    from app.services.auth import hash_password

    with Session(engine) as session:
        default_tenant = session.exec(select(Tenant).where(Tenant.id == 1)).first()
        if not default_tenant:
            default_tenant = Tenant(
                id=1,
                name="الشركة الافتراضية",
                code="default",
                industry="مقاولات",
                status=TenantStatus.ACTIVE,
                subscription_type="basic",
                is_default=True,
            )
            session.add(default_tenant)
            session.commit()
            session.refresh(default_tenant)

        config = session.exec(select(CompanyConfig).where(CompanyConfig.tenant_id == default_tenant.id)).first()
        if not config:
            session.add(CompanyConfig(tenant_id=default_tenant.id))
            session.commit()

        admin_user = session.exec(select(User).where(User.username == "admin")).first()
        if not admin_user:
            session.add(User(
                username="admin",
                hashed_password=hash_password("admin123"),
                role="admin",
                tenant_id=default_tenant.id,
            ))
            session.commit()


def get_session() -> Generator[Session, None, None]:
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()