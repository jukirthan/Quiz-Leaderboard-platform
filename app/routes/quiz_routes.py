from flask import Blueprint
from app.middleware import auth_required, creator_required
from app.controllers import quiz_controller

quizzes_bp = Blueprint("quizzes", __name__)


@quizzes_bp.route("/quizzes", methods=["GET"])
def list_quizzes():
    return quiz_controller.list_quizzes()


@quizzes_bp.route("/quizzes/<int:quiz_id>", methods=["GET"])
def get_quiz(quiz_id):
    return quiz_controller.get_quiz(quiz_id)


@quizzes_bp.route("/quizzes/category/<int:category_id>", methods=["GET"])
def get_quizzes_by_category(category_id):
    return quiz_controller.get_quizzes_by_category(category_id)


@quizzes_bp.route("/quizzes", methods=["POST"])
@auth_required
def create_quiz():
    return quiz_controller.create_quiz()


@quizzes_bp.route("/quizzes/<int:quiz_id>", methods=["PUT"])
@creator_required
def update_quiz(quiz_id):
    return quiz_controller.update_quiz(quiz_id)


@quizzes_bp.route("/quizzes/<int:quiz_id>", methods=["DELETE"])
@creator_required
def delete_quiz(quiz_id):
    return quiz_controller.delete_quiz(quiz_id)


@quizzes_bp.route("/my/quizzes", methods=["GET"])
@auth_required
def my_quizzes():
    return quiz_controller.my_quizzes()
