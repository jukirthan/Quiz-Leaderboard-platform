from flask import request, jsonify
from app.extensions import db
from app.models.quiz import Quiz
from app.models.question import Question, AnswerEnum


def _parse_answer(value):
    if not value:
        return None
    val = str(value).upper().strip()
    if val in ("A", "B", "C", "D"):
        return AnswerEnum(val)
    return None


def add_question(quiz_id):
    Quiz.query.get_or_404(quiz_id)
    data = request.get_json() or {}

    question_text = data.get("question_text", "").strip()
    if not question_text:
        return jsonify({"error": "question_text is required"}), 400

    correct = _parse_answer(data.get("correct_answer"))
    if not correct:
        return jsonify({"error": "correct_answer must be A, B, C, or D"}), 400

    for field in ("option_a", "option_b", "option_c", "option_d"):
        if not data.get(field, "").strip():
            return jsonify({"error": f"{field} is required"}), 400

    question = Question(
        quiz_id=quiz_id,
        question_text=question_text,
        option_a=data["option_a"].strip(),
        option_b=data["option_b"].strip(),
        option_c=data["option_c"].strip(),
        option_d=data["option_d"].strip(),
        correct_answer=correct,
        marks=data.get("marks", 1),
    )
    db.session.add(question)
    db.session.commit()
    return jsonify(question.to_dict(include_answer=True)), 201


def update_question(question_id):
    question = Question.query.get_or_404(question_id)
    data = request.get_json() or {}

    if "question_text" in data:
        question.question_text = data["question_text"].strip()
    for field in ("option_a", "option_b", "option_c", "option_d"):
        if field in data:
            setattr(question, field, data[field].strip())
    if "correct_answer" in data:
        correct = _parse_answer(data["correct_answer"])
        if not correct:
            return jsonify({"error": "correct_answer must be A, B, C, or D"}), 400
        question.correct_answer = correct
    if "marks" in data:
        question.marks = data["marks"]

    db.session.commit()
    return jsonify(question.to_dict(include_answer=True)), 200


def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return jsonify({"message": "Question deleted"}), 200
