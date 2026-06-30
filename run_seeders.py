from app import create_app
from app.extensions import db
from app.seeders.admin_seeder import seed_admin
from app.seeders.category_seeder import seed_categories
from app.seeders.quiz_seeder import seed_quizzes

app = create_app()

with app.app_context():
    from sqlalchemy import text

    legacy_tables = [
        "user_answers", "quiz_attempts", "attempt_answers", "attempts",
        "options", "questions", "leaderboard", "quizzes", "categories", "users",
    ]
    db.session.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
    for table in legacy_tables:
        db.session.execute(text(f"DROP TABLE IF EXISTS `{table}`"))
    db.session.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
    db.session.commit()

    db.create_all()
    seed_admin()
    seed_categories()
    seed_quizzes()
    print("Seeding complete.")
