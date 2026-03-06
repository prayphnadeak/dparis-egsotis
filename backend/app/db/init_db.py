"""Database initialization and first-run setup."""
import logging

from sqlalchemy import text

from app.db.session import engine, SessionLocal
from app.db import base  # noqa – ensures all models are registered
from app.models.base import Base
from app.models.user import User, UserRole
from app.core.security import hash_password
from app.core.config import settings

logger = logging.getLogger("dparis.db")


async def init_db() -> None:
    """Create all tables and seed admin user if not present."""
    try:
        # Create tables (Always for SQLite, or if not in production for other DBs)
        if settings.DATABASE_URL.startswith("sqlite") or settings.ENVIRONMENT != "production":
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables created / verified.")
        else:
            logger.info("Skipping table creation in production (read-only FS).")

        # Seed admin user
        db = SessionLocal()
        try:
            # Seed admin
            existing_admin = db.query(User).filter(User.username == settings.ADMIN_USERNAME).first()
            if not existing_admin:
                admin = User(
                    username=settings.ADMIN_USERNAME,
                    email=settings.ADMIN_EMAIL,
                    hashed_password=hash_password(settings.ADMIN_PASSWORD),
                    full_name="Administrator",
                    role=UserRole.ADMIN,
                    is_active=True,
                )
                db.add(admin)
                db.commit()
                logger.info("Admin user created: %s", settings.ADMIN_USERNAME)

            # Seed data if accommodations table is empty
            from app.models.accommodation import Accommodation
            if db.query(Accommodation).count() == 0:
                logger.info("Database empty, starting auto-seeding...")
                from scripts.seed_all import seed as run_seeding
                run_seeding()
        finally:
            db.close()
    except Exception as exc:
        logger.error("Database init failed: %s", exc)
        raise
