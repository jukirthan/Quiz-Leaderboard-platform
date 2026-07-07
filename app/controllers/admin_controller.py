from app.extensions import db
from app.models.quiz import Quiz, Question
from app.models.category import Category
from app.utils import success_response, error_response


def create_quiz(data, user_id):
    title = data.get("title")
    category_id = data.get("category_id")
    questions = data.get("questions", [])

    if not title or not category_id:
        return error_response("title and category_id are required")

    if not Category.query.get(category_id):
        return error_response("Category not found", 404)

    if len(questions) == 0:
        return error_response("At least one question is required")

    quiz = Quiz(
        title=title,
        description=data.get("description", ""),
        category_id=category_id,
        creator_id=user_id,
        time_limit=data.get("time_limit", 0),
        shuffle_questions=data.get("shuffle_questions", False)
    )
    db.session.add(quiz)
    db.session.flush()

    for q in questions:
        question = Question(
            question_text=q.get("question_text"),
            option_a=q.get("option_a"),
            option_b=q.get("option_b"),
            option_c=q.get("option_c"),
            option_d=q.get("option_d"),
            correct_option=q.get("correct_option", "").lower(),
            quiz_id=quiz.id
        )
        db.session.add(question)

    db.session.commit()

    return success_response("Quiz created successfully", quiz.to_dict(), 201)
