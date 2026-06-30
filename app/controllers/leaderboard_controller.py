from flask import jsonify
from app.models.user_model import User
from app.models.quiz_model import Quiz
from app.models.attempt_model import QuizAttempt
from app.controllers.attempt_controller import _quiz_leaderboard_entries


def get_leaderboard():
    """Global leaderboard — top users ranked by total score across all quizzes."""
    attempts = (
        QuizAttempt.query
        .filter(QuizAttempt.completed_at.isnot(None))
        .all()
    )

    user_scores = {}
    for a in attempts:
        uid = a.user_id
        if uid not in user_scores:
            user_scores[uid] = {
                "user_id": uid,
                "username": a.user.username if a.user else None,
                "total_score": 0,
                "quizzes_taken": 0,
            }
        user_scores[uid]["total_score"] += a.score or 0
        user_scores[uid]["quizzes_taken"] += 1

    ranked = sorted(user_scores.values(), key=lambda x: -x["total_score"])
    for rank, entry in enumerate(ranked, start=1):
        entry["rank"] = rank

    return jsonify(ranked[:50]), 200


def quiz_leaderboard(quiz_id):
    Quiz.query.get_or_404(quiz_id)
    entries = _quiz_leaderboard_entries(quiz_id)[:50]
    return jsonify(entries), 200


def category_leaderboard(category_id):
    from app.models.category_model import Category
    Category.query.get_or_404(category_id)

    quiz_ids = [q.id for q in Quiz.query.filter_by(category_id=category_id).all()]
    if not quiz_ids:
        return jsonify([]), 200

    attempts = (
        QuizAttempt.query
        .filter(QuizAttempt.quiz_id.in_(quiz_ids))
        .filter(QuizAttempt.completed_at.isnot(None))
        .all()
    )

    user_scores = {}
    for a in attempts:
        uid = a.user_id
        if uid not in user_scores:
            user_scores[uid] = {
                "user_id": uid,
                "username": a.user.username if a.user else None,
                "total_score": 0,
            }
        user_scores[uid]["total_score"] += a.score or 0

    ranked = sorted(user_scores.values(), key=lambda x: -x["total_score"])
    for rank, entry in enumerate(ranked, start=1):
        entry["rank"] = rank

    return jsonify(ranked[:50]), 200
