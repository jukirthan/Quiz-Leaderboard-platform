from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, current_user
from app.models.quiz import Quiz


def owner_required(f):
    @wraps(f)
    def decorated(quiz_id, *args, **kwargs):
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return jsonify({"success": False, "message": "Quiz not found"}), 404
        user_id = get_jwt_identity()
        is_owner = str(quiz.creator_id) == str(user_id)
        is_admin = current_user and current_user.is_admin()
        if not is_owner and not is_admin:
            return jsonify({"success": False, "message": "You are not allowed to modify this quiz"}), 403
        return f(quiz_id, *args, **kwargs)
    return decorated


def admin_required(f):
    """Requires a valid JWT (apply @jwt_required() above this) and an admin role."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user or not current_user.is_admin():
            return jsonify({"success": False, "message": "Admin access required"}), 403
        return f(*args, **kwargs)
    return decorated


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"success": False, "message": "Resource not found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"success": False, "message": "Internal server error"}), 500

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"success": False, "message": "Method not allowed"}), 405
