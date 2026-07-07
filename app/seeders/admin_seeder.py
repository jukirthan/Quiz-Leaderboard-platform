import os

from app.extensions import db, bcrypt
from app.models.user import User

DEFAULT_ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
DEFAULT_ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@gmail.com")
DEFAULT_ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")


def seed_admin():
    exists = User.query.filter_by(email=DEFAULT_ADMIN_EMAIL).first()
    if not exists:
        hashed_password = bcrypt.generate_password_hash(DEFAULT_ADMIN_PASSWORD).decode("utf-8")
        admin = User(
            username=DEFAULT_ADMIN_USERNAME,
            email=DEFAULT_ADMIN_EMAIL,
            password=hashed_password,
            role="admin"
        )
        db.session.add(admin)
    db.session.commit()
    print("Admin seeded successfully")
