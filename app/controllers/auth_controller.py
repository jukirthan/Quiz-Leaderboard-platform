import os
from flask_jwt_extended import create_access_token
from app.extensions import db, bcrypt
from app.models.user import User
from app.utils import success_response, error_response


def register_user(data):
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    admin_code = data.get("admin_code")

    if not username or not email or not password:
        return error_response("username, email and password are required")

    if User.query.filter_by(email=email).first():
        return error_response("Email already registered")

    if User.query.filter_by(username=username).first():
        return error_response("Username already taken")

    configured_admin_code = os.environ.get("ADMIN_SIGNUP_CODE")
    role = "admin" if configured_admin_code and admin_code == configured_admin_code else "user"

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(username=username, email=email, password=hashed_password, role=role)

    db.session.add(user)
    db.session.commit()

    return success_response("User registered successfully", user.to_dict(), 201)


def login_user(data):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return error_response("email and password are required")

    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return error_response("Invalid email or password", 401)

    access_token = create_access_token(identity=str(user.id))

    return success_response("Login successful", {
        "token": access_token,
        "user": user.to_dict()
    })
