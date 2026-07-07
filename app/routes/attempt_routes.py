from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.attempt_controller import (
    submit_attempt,
    get_leaderboard,
    get_category_leaderboard,
    get_user_attempts
)

attempt_bp = Blueprint("attempt_bp", __name__)


@attempt_bp.route("/", methods=["POST"])
@jwt_required()
def create_attempt():
    data = request.get_json()
    user_id = int(get_jwt_identity())
    return submit_attempt(data, user_id)


@attempt_bp.route("/leaderboard/quiz/<int:quiz_id>", methods=["GET"])
def quiz_leaderboard(quiz_id):
    return get_leaderboard(quiz_id)


@attempt_bp.route("/leaderboard/category/<int:category_id>", methods=["GET"])
def category_leaderboard(category_id):
    return get_category_leaderboard(category_id)


@attempt_bp.route("/my-attempts", methods=["GET"])
@jwt_required()
def my_attempts():
    user_id = int(get_jwt_identity())
    return get_user_attempts(user_id)