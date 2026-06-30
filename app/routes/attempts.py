from flask import Blueprint
from app.middleware import auth_required, attempt_owner_required
from app.controllers import attempt_controller

attempts_bp = Blueprint("attempts", __name__)


@attempts_bp.route("/quizzes/<int:quiz_id>/start", methods=["POST"])
@auth_required
def start_attempt(quiz_id):
    return attempt_controller.start_attempt(quiz_id)


@attempts_bp.route("/quizzes/<int:quiz_id>/submit", methods=["POST"])
@auth_required
def submit_attempt(quiz_id):
    return attempt_controller.submit_attempt(quiz_id)


@attempts_bp.route("/my/attempts", methods=["GET"])
@auth_required
def my_attempts():
    return attempt_controller.my_attempts()


@attempts_bp.route("/attempts/<int:attempt_id>", methods=["GET"])
@attempt_owner_required
def get_attempt(attempt_id):
    return attempt_controller.get_attempt(attempt_id)
