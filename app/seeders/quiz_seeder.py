from app.extensions import db
from app.models.user_model import User, RoleEnum
from app.models.category_model import Category
from app.models.quiz_model import Quiz
from app.models.question_model import Question, AnswerEnum


def seed_quizzes():
    if Quiz.query.count() > 0:
        return

    admin = User.query.filter_by(role=RoleEnum.admin).first()
    if not admin:
        return

    science = Category.query.filter_by(name="Science").first()
    if not science:
        return

    quiz = Quiz(
        creator_id=admin.id,
        category_id=science.id,
        title="Basic Science Quiz",
        description="Test your knowledge of fundamental science concepts",
        is_public=True,
        time_limit=10,
    )
    db.session.add(quiz)
    db.session.flush()

    questions = [
        {
            "question_text": "What is the chemical symbol for water?",
            "option_a": "H2O",
            "option_b": "CO2",
            "option_c": "O2",
            "option_d": "NaCl",
            "correct_answer": AnswerEnum.A,
            "marks": 1,
        },
        {
            "question_text": "Which planet is known as the Red Planet?",
            "option_a": "Venus",
            "option_b": "Mars",
            "option_c": "Jupiter",
            "option_d": "Saturn",
            "correct_answer": AnswerEnum.B,
            "marks": 1,
        },
        {
            "question_text": "What gas do plants absorb from the atmosphere?",
            "option_a": "Oxygen",
            "option_b": "Nitrogen",
            "option_c": "Carbon Dioxide",
            "option_d": "Hydrogen",
            "correct_answer": AnswerEnum.C,
            "marks": 2,
        },
    ]

    for q in questions:
        db.session.add(Question(quiz_id=quiz.id, **q))

    db.session.commit()
    print("Seeded sample quiz with questions")
