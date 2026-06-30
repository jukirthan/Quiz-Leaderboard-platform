from app.extensions import db, bcrypt
from app.models.user_model import User, RoleEnum


def seed_admin():
    if User.query.filter_by(role=RoleEnum.admin).first():
        return

    admin = User(
        username="admin",
        email="admin@quizhub.com",
        password=bcrypt.generate_password_hash("admin123").decode("utf-8"),
        role=RoleEnum.admin,
        is_active=True,
    )
    db.session.add(admin)
    db.session.commit()
    print("Admin user created: admin@quizhub.com / admin123")
