from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.quiz import Quiz
from app.models.quiz_attempt import QuizAttempt
from app.utils import success_response

dashboard_bp = Blueprint("dashboard_bp", __name__)


@dashboard_bp.route("/", methods=["GET"])
@jwt_required()
def get_dashboard():
    user_id = int(get_jwt_identity())

    created_quizzes = Quiz.query.filter_by(creator_id=user_id).order_by(Quiz.created_at.desc()).all()
    attempts = QuizAttempt.query.filter_by(user_id=user_id).order_by(QuizAttempt.attempted_at.desc()).all()

    data = {
        "quizzes_created": [q.to_dict() for q in created_quizzes],
        "attempts_taken": [a.to_dict() for a in attempts],
        "total_quizzes_created": len(created_quizzes),
        "total_attempts_taken": len(attempts)
    }

    return success_response("Dashboard fetched", data)
