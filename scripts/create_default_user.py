#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlmodel import Session, select
from app.database import engine
from app.models.user import User
from app.services.auth import hash_password

def create_default_user():
    with Session(engine) as session:
        # Check if user exists
        existing = session.exec(
            select(User).where(User.username == "admin")
        ).first()
        if existing:
            print("Default user already exists.")
            return

        # Create default user
        user = User(
            username="admin",
            hashed_password=hash_password("admin123"),
            role="admin",
            tenant_id=1
        )
        session.add(user)
        session.commit()
        print("Default user created: username=admin, password=admin123")

if __name__ == "__main__":
    create_default_user()