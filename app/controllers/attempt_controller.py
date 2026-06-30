from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from datetime import datetime
from decimal import Decimal
from app.extensions import db
from app.models.user_model import User
from app.models.quiz_model import Quiz
from app.models.question_model import Question, AnswerEnum
from app.models.attempt_model import QuizAttempt, UserAnswer


def _current_user():
    return User.query.get(get_jwt_identity())


def _parse_answer(value):
    if not value:
        return None
    val = str(value).upper().strip()
    if val in ("A", "B", "C", "D"):
        return AnswerEnum(val)
    return None


def start_attempt(quiz_id):
    user = _current_user()
    quiz = Quiz.query.get_or_404(quiz_id)

    if not quiz.is_public:
        return jsonify({"error": "Quiz is not public"}), 400

    if len(quiz.questions) == 0:
        return jsonify({"error": "Quiz has no questions yet"}), 400

    total_marks = sum(q.marks for q in quiz.questions)
    attempt = QuizAttempt(
        user_id=user.id,
        quiz_id=quiz.id,
        total_marks=total_marks,
    )
    db.session.add(attempt)
    db.session.commit()

    questions = []
    for q in quiz.questions:
        questions.append({
            "id": q.id,
            "question_text": q.question_text,
            "marks": q.marks,
            "options": q.options_for_play(),
        })

    return jsonify({
        "attempt_id": attempt.id,
        "quiz_id": quiz.id,
        "total_marks": total_marks,
        "time_limit": quiz.time_limit,
        "questions": questions,
    }), 201


def submit_attempt(quiz_id):
    user = _current_user()
    quiz = Quiz.query.get_or_404(quiz_id)
    data = request.get_json() or {}

    attempt_id = data.get("attempt_id")
    if not attempt_id:
        return jsonify({"error": "attempt_id is required"}), 400

    attempt = QuizAttempt.query.get_or_404(attempt_id)
    if attempt.user_id != user.id or attempt.quiz_id != quiz.id:
        return jsonify({"error": "Invalid attempt"}), 403

    if attempt.completed_at:
        return jsonify({"error": "Attempt already submitted"}), 400

    answers_data = data.get("answers", [])
    score = 0
    results = []

    for ans in answers_data:
        question_id = ans.get("question_id")
        selected = _parse_answer(ans.get("selected_answer"))
        if not question_id or not selected:
            continue

        question = Question.query.get(question_id)
        if not question or question.quiz_id != quiz.id:
            continue

        is_correct = selected == question.correct_answer
        if is_correct:
            score += question.marks

        db.session.add(UserAnswer(
            attempt_id=attempt.id,
            question_id=question_id,
            selected_answer=selected,
            is_correct=is_correct,
        ))
        results.append({
            "question_id": question_id,
            "selected_answer": selected.value,
            "correct_answer": question.correct_answer.value,
            "is_correct": is_correct,
            "marks": question.marks if is_correct else 0,
        })

    total_marks = attempt.total_marks or 1
    percentage = Decimal(str(round((score / total_marks) * 100, 2)))

    attempt.score = score
    attempt.percentage = percentage
    attempt.completed_at = datetime.utcnow()
    db.session.commit()

    leaderboard = _quiz_leaderboard_entries(quiz.id)
    rank = next((e["rank"] for e in leaderboard if e["user_id"] == user.id), None)

    return jsonify({
        "attempt_id": attempt.id,
        "score": score,
        "total_marks": total_marks,
        "percentage": float(percentage),
        "answers": results,
        "leaderboard_rank": rank,
    }), 200


def my_attempts():
    user = _current_user()
    attempts = (
        QuizAttempt.query
        .filter_by(user_id=user.id)
        .filter(QuizAttempt.completed_at.isnot(None))
        .order_by(QuizAttempt.completed_at.desc())
        .all()
    )
    return jsonify([a.to_dict() for a in attempts]), 200


def get_attempt(attempt_id):
    attempt = QuizAttempt.query.get_or_404(attempt_id)
    data = attempt.to_dict()
    data["answers"] = []
    for ua in attempt.answers:
        q = Question.query.get(ua.question_id)
        data["answers"].append({
            "question_id": ua.question_id,
            "question_text": q.question_text if q else None,
            "selected_answer": ua.selected_answer.value,
            "correct_answer": q.correct_answer.value if q else None,
            "is_correct": ua.is_correct,
        })
    return jsonify(data), 200


def _quiz_leaderboard_entries(quiz_id):
    attempts = (
        QuizAttempt.query
        .filter_by(quiz_id=quiz_id)
        .filter(QuizAttempt.completed_at.isnot(None))
        .order_by(
            QuizAttempt.score.desc(),
            QuizAttempt.percentage.desc(),
            QuizAttempt.completed_at.asc(),
        )
        .all()
    )

    best_by_user = {}
    for a in attempts:
        uid = a.user_id
        if uid not in best_by_user or a.score > best_by_user[uid].score:
            best_by_user[uid] = a

    ranked = sorted(
        best_by_user.values(),
        key=lambda a: (-a.score, -float(a.percentage), a.completed_at),
    )

    entries = []
    for rank, a in enumerate(ranked, start=1):
        entries.append({
            "rank": rank,
            "user_id": a.user_id,
            "username": a.user.username if a.user else None,
            "score": a.score,
            "total_marks": a.total_marks,
            "percentage": float(a.percentage),
            "completed_at": a.completed_at.isoformat() if a.completed_at else None,
        })
    return entries
