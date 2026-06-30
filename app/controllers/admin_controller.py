from flask import jsonify
from app.extensions import db
from app.models.user import User
from app.models.quiz import Quiz


def list_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return jsonify([u.to_dict() for u in users]), 200


def list_all_quizzes():
    quizzes = Quiz.query.order_by(Quiz.created_at.desc()).all()
    return jsonify([q.to_dict() for q in quizzes]), 200


def admin_delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    return jsonify({"message": "Quiz deleted"}), 200


def admin_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200
