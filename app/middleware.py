from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models.user import User
from app.models.quiz import Quiz
from app.models.attempt import QuizAttempt


def _get_current_user():
    user_id = get_jwt_identity()
    if user_id is None:
        return None
    return User.query.get(int(user_id))


def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user = _get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401
        if not user.is_active:
            return jsonify({"error": "Account is deactivated"}), 403
        return fn(*args, **kwargs)
    return wrapper


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user = _get_current_user()
        if not user or user.role.value != "admin":
            return jsonify({"error": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper


def creator_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user = _get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401

        quiz_id = kwargs.get("quiz_id")
        if quiz_id is None:
            return jsonify({"error": "Quiz not found"}), 404

        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return jsonify({"error": "Quiz not found"}), 404

        if user.role.value != "admin" and quiz.creator_id != user.id:
            return jsonify({"error": "Only the quiz creator can perform this action"}), 403

        return fn(*args, **kwargs)
    return wrapper


def question_creator_required(fn):
    """Admin only for question management (per project requirement)."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user = _get_current_user()
        if not user or user.role.value != "admin":
            return jsonify({"error": "Only admins can manage questions"}), 403
        return fn(*args, **kwargs)
    return wrapper


def attempt_owner_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user = _get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401

        attempt_id = kwargs.get("attempt_id")
        attempt = QuizAttempt.query.get(attempt_id)
        if not attempt:
            return jsonify({"error": "Attempt not found"}), 404

        if user.role.value != "admin" and attempt.user_id != user.id:
            return jsonify({"error": "Forbidden"}), 403

        return fn(*args, **kwargs)
    return wrapper
