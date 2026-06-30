from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app.models.user import User
from app.models.quiz import Quiz
from app.models.attempt import QuizAttempt
from app.controllers.attempt_controller import _quiz_leaderboard_entries


def dashboard():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)

    created_quizzes = Quiz.query.filter_by(creator_id=user_id).order_by(Quiz.created_at.desc()).all()
    attempts = (
        QuizAttempt.query
        .filter_by(user_id=user_id)
        .filter(QuizAttempt.completed_at.isnot(None))
        .order_by(QuizAttempt.completed_at.desc())
        .all()
    )

    highest_score = 0
    if attempts:
        highest_score = max(float(a.percentage) for a in attempts)

    return jsonify({
        "user": user.to_dict(),
        "stats": {
            "quizzes_created": len(created_quizzes),
            "total_attempts": len(attempts),
            "highest_score": highest_score,
        },
        "created_quizzes": [q.to_dict() for q in created_quizzes[:5]],
        "recent_attempts": [a.to_dict() for a in attempts[:5]],
    }), 200
