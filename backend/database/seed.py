"""
Database seeding - creates default admin user and sample data.
"""

from sqlalchemy.orm import Session
from backend.models.user import User, UserRole
from backend.config import settings
from backend.services.auth_service import hash_password


def seed_admin_user(db: Session) -> None:
    """Create default admin user if it doesn't exist."""
    existing = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()
    if not existing:
        admin = User(
            email=settings.ADMIN_EMAIL,
            name="Admin",
            password_hash=hash_password(settings.ADMIN_PASSWORD),
            role=UserRole.ADMIN,
            is_active=True,
        )
        db.add(admin)
        db.commit()
        print(f"[SEED] Admin user created: {settings.ADMIN_EMAIL}")
    else:
        print(f"[SEED] Admin user already exists: {settings.ADMIN_EMAIL}")


def run_seeds(db: Session) -> None:
    """Run all database seeds."""
    seed_admin_user(db)
    print("[SEED] Database seeding complete.")
