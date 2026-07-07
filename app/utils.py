import random
from sqlalchemy import inspect, text


def ensure_role_column(db):
    """Adds the 'role' column to an already-existing 'users' table (safe to run repeatedly)."""
    inspector = inspect(db.engine)
    if "users" not in inspector.get_table_names():
        return

    columns = [col["name"] for col in inspector.get_columns("users")]
    if "role" in columns:
        return

    with db.engine.connect() as conn:
        conn.execute(text(
            "ALTER TABLE users ADD COLUMN role VARCHAR(20) NOT NULL DEFAULT 'user'"
        ))
        conn.commit()


def success_response(message, data=None, status_code=200):
    body = {"success": True, "message": message}
    if data is not None:
        body["data"] = data
    return body, status_code


def error_response(message, status_code=400):
    return {"success": False, "message": message}, status_code


def calculate_score(questions, answers):
    score = 0
    for question in questions:
        submitted = answers.get(str(question.id))
        if submitted and submitted.lower() == question.correct_option.lower():
            score += 1
    return score


def get_badge(percentage):
    if percentage >= 80:
        return "Gold"
    elif percentage >= 50:
        return "Silver"
    else:
        return "Bronze"


def shuffle_list(items):
    shuffled = items[:]
    random.shuffle(shuffled)
    return shuffled
