"""
Run: python -m scripts.create_admin
Creates default admin user.
"""
from app.database import SessionLocal, Base, engine
from app.models.user import User, UserRole
from app.core.security import hash_password
from app import models  # noqa

Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    existing = db.query(User).filter(User.username == "admin").first()
    if existing:
        print("Admin already exists.")
    else:
        admin = User(
            username="admin",
            email="admin@noms.local",
            full_name="System Admin",
            role=UserRole.admin,
            password_hash=hash_password("admin123"),
        )
        db.add(admin)
        db.commit()
        print("✅ Admin created: username=admin password=admin123")
finally:
    db.close()