from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.extensions import db
from app.models.user import User
from app.models.quiz import Quiz


def _current_user():
    return User.query.get(int(get_jwt_identity()))


def list_quizzes():
    category_id = request.args.get("category_id", type=int)
    search = request.args.get("search", "").strip()

    query = Quiz.query.filter_by(is_public=True)
    if category_id:
        query = query.filter_by(category_id=category_id)
    if search:
        query = query.filter(Quiz.title.ilike(f"%{search}%"))

    quizzes = query.order_by(Quiz.created_at.desc()).all()
    return jsonify([q.to_dict() for q in quizzes]), 200


def get_quizzes_by_category(category_id):
    from app.models.category import Category
    Category.query.get_or_404(category_id)
    quizzes = (
        Quiz.query.filter_by(category_id=category_id, is_public=True)
        .order_by(Quiz.created_at.desc())
        .all()
    )
    return jsonify([q.to_dict() for q in quizzes]), 200


def get_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    user = _current_user_optional()
    include_answers = user and (user.role.value == "admin" or quiz.creator_id == user.id)
    data = quiz.to_dict()
    data["questions"] = []
    for q in quiz.questions:
        qdata = q.to_dict(include_answer=include_answers)
        if not include_answers:
            qdata["options"] = q.options_for_play()
        data["questions"].append(qdata)
    return jsonify(data), 200


def _current_user_optional():
    try:
        from flask_jwt_extended import verify_jwt_in_request
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        return User.query.get(int(identity)) if identity is not None else None
    except Exception:
        return None


def create_quiz():
    user = _current_user()
    data = request.get_json() or {}

    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "title is required"}), 400

    quiz = Quiz(
        creator_id=user.id,
        title=title,
        description=data.get("description", ""),
        category_id=data.get("category_id"),
        time_limit=data.get("time_limit"),
        is_public=data.get("is_public", False),
    )
    db.session.add(quiz)
    db.session.commit()
    return jsonify(quiz.to_dict()), 201


def update_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    data = request.get_json() or {}

    if "title" in data:
        quiz.title = data["title"].strip()
    if "description" in data:
        quiz.description = data["description"]
    if "category_id" in data:
        quiz.category_id = data["category_id"]
    if "time_limit" in data:
        quiz.time_limit = data["time_limit"]
    if "is_public" in data:
        quiz.is_public = data["is_public"]

    db.session.commit()
    return jsonify(quiz.to_dict_with_questions(include_answers=True)), 200


def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    return jsonify({"message": "Quiz deleted"}), 200


def my_quizzes():
    user = _current_user()
    quizzes = Quiz.query.filter_by(creator_id=user.id).order_by(Quiz.created_at.desc()).all()
    return jsonify([q.to_dict() for q in quizzes]), 200
