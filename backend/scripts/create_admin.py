"""Script to create or reset the admin user."""
import sys
import os
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session import SessionLocal
from app.db.init_db import init_db
from app.models.user import User, UserRole
from app.core.security import hash_password
from app.core.config import settings


def create_admin(username: str = None, email: str = None, password: str = None):
    username = username or settings.ADMIN_USERNAME
    email = email or settings.ADMIN_EMAIL
    password = password or settings.ADMIN_PASSWORD

    asyncio.run(init_db())
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.username == username).first()
        if existing:
            existing.hashed_password = hash_password(password)
            existing.role = UserRole.ADMIN
            existing.is_active = True
            db.commit()
            print(f"✅ Admin diperbarui: {username}")
        else:
            admin = User(
                username=username,
                email=email,
                hashed_password=hash_password(password),
                full_name="Administrator",
                role=UserRole.ADMIN,
                is_active=True,
            )
            db.add(admin)
            db.commit()
            print(f"✅ Admin dibuat: {username}")
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Create or reset admin user")
    parser.add_argument("--username", default=None)
    parser.add_argument("--email", default=None)
    parser.add_argument("--password", default=None)
    args = parser.parse_args()
    create_admin(args.username, args.email, args.password)
