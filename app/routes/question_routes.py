from flask import Blueprint
from app.middleware import auth_required, creator_required
from app.controllers import question_controller

questions_bp = Blueprint("questions", __name__)


@questions_bp.route("/quizzes/<int:quiz_id>/questions", methods=["POST"])
@creator_required
def add_question(quiz_id):
    return question_controller.add_question(quiz_id)


@questions_bp.route("/questions/<int:question_id>", methods=["PUT"])
@auth_required
def update_question(question_id):
    return question_controller.update_question(question_id)


@questions_bp.route("/questions/<int:question_id>", methods=["DELETE"])
@auth_required
def delete_question(question_id):
    return question_controller.delete_question(question_id)
