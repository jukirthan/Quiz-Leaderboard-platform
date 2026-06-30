from flask import Blueprint
from app.controllers import leaderboard_controller

leaderboard_bp = Blueprint("leaderboard", __name__)


@leaderboard_bp.route("/leaderboard/quiz/<int:quiz_id>", methods=["GET"])
def quiz_leaderboard(quiz_id):
    return leaderboard_controller.quiz_leaderboard(quiz_id)


@leaderboard_bp.route("/leaderboard/category/<int:category_id>", methods=["GET"])
def category_leaderboard(category_id):
    return leaderboard_controller.category_leaderboard(category_id)
