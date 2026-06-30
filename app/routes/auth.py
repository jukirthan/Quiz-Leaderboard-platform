from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers import auth_controller

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    return auth_controller.register()


@auth_bp.route("/login", methods=["POST"])
def login():
    return auth_controller.login()


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    return auth_controller.logout()


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    return auth_controller.profile()
