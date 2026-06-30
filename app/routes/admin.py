from flask import Blueprint
from app.middleware import admin_required
from app.controllers import admin_controller

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin/users", methods=["GET"])
@admin_required
def list_users():
    return admin_controller.list_users()


@admin_bp.route("/admin/quizzes", methods=["GET"])
@admin_required
def list_all_quizzes():
    return admin_controller.list_all_quizzes()


@admin_bp.route("/admin/quizzes/<int:quiz_id>", methods=["DELETE"])
@admin_required
def admin_delete_quiz(quiz_id):
    return admin_controller.admin_delete_quiz(quiz_id)


@admin_bp.route("/admin/users/<int:user_id>", methods=["DELETE"])
@admin_required
def admin_delete_user(user_id):
    return admin_controller.admin_delete_user(user_id)
