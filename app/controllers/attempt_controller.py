from app.extensions import db
from app.models.quiz import Quiz
from app.models.quiz_attempt import QuizAttempt
from app.models.user import User
from app.utils import success_response, error_response, calculate_score, get_badge


def submit_attempt(data, user_id):
    quiz_id = data.get("quiz_id")
    answers = data.get("answers", {})
    time_taken = data.get("time_taken", 0)

    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return error_response("Quiz not found", 404)

    questions = quiz.questions
    total_questions = len(questions)

    if total_questions == 0:
        return error_response("This quiz has no questions")

    score = calculate_score(questions, answers)
    percentage = round((score / total_questions) * 100, 2)

    attempt = QuizAttempt(
        score=score,
        total_questions=total_questions,
        percentage=percentage,
        time_taken=time_taken,
        user_id=user_id,
        quiz_id=quiz_id
    )
    db.session.add(attempt)
    db.session.commit()

    result = attempt.to_dict()
    result["badge"] = get_badge(percentage)

    return success_response("Quiz submitted successfully", result, 201)


def get_leaderboard(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return error_response("Quiz not found", 404)

    attempts = QuizAttempt.query.filter_by(quiz_id=quiz_id).order_by(
        QuizAttempt.score.desc(), QuizAttempt.time_taken.asc()
    ).all()

    leaderboard = []
    for rank, attempt in enumerate(attempts, start=1):
        user = User.query.get(attempt.user_id)
        leaderboard.append({
            "rank": rank,
            "username": user.username if user else "Unknown",
            "score": attempt.score,
            "total_questions": attempt.total_questions,
            "percentage": attempt.percentage,
            "badge": get_badge(attempt.percentage),
            "time_taken": attempt.time_taken,
            "attempted_at": attempt.attempted_at
        })

    return success_response("Leaderboard fetched", leaderboard)


def get_category_leaderboard(category_id):
    attempts = QuizAttempt.query.join(Quiz).filter(Quiz.category_id == category_id).order_by(
        QuizAttempt.percentage.desc()
    ).all()

    leaderboard = []
    for rank, attempt in enumerate(attempts, start=1):
        user = User.query.get(attempt.user_id)
        leaderboard.append({
            "rank": rank,
            "username": user.username if user else "Unknown",
            "quiz_id": attempt.quiz_id,
            "score": attempt.score,
            "percentage": attempt.percentage,
            "badge": get_badge(attempt.percentage)
        })

    return success_response("Category leaderboard fetched", leaderboard)


def get_user_attempts(user_id):
    attempts = QuizAttempt.query.filter_by(user_id=user_id).order_by(QuizAttempt.attempted_at.desc()).all()
    return success_response("Attempts fetched", [a.to_dict() for a in attempts])
