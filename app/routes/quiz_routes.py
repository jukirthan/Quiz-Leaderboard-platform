from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.quiz_controller import (
    create_quiz,
    get_all_quizzes,
    get_quizzes_by_category,
    get_quiz_for_attempt,
    get_quiz_detail,
    delete_quiz
)
from app.middleware import owner_required, admin_required

quiz_bp = Blueprint("quiz_bp", __name__)


@quiz_bp.route("/", methods=["GET"])
def list_quizzes():
    category_id = request.args.get("category_id")
    if category_id:
        return get_quizzes_by_category(category_id)
    return get_all_quizzes()


@quiz_bp.route("/", methods=["POST"])
@jwt_required()
@admin_required
def add_quiz():
    data = request.get_json()
    user_id = int(get_jwt_identity())
    return create_quiz(data, user_id)


@quiz_bp.route("/<int:quiz_id>", methods=["GET"])
def take_quiz(quiz_id):
    return get_quiz_for_attempt(quiz_id)


@quiz_bp.route("/<int:quiz_id>/detail", methods=["GET"])
@jwt_required()
def quiz_detail(quiz_id):
    return get_quiz_detail(quiz_id)


@quiz_bp.route("/<int:quiz_id>", methods=["DELETE"])
@jwt_required()
@owner_required
def remove_quiz(quiz_id):
    return delete_quiz(quiz_id)