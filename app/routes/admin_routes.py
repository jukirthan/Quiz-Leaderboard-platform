from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.admin_controller import create_quiz
from app.middleware import admin_required

admin_bp = Blueprint("admin_bp", __name__)


@admin_bp.route("/quizzes", methods=["POST"])
@jwt_required()
@admin_required
def add_quiz():
    data = request.get_json()
    user_id = int(get_jwt_identity())
    return create_quiz(data, user_id)
