from datetime import datetime
from app.extensions import db


class QuizAttempt(db.Model):
    __tablename__ = "quiz_attempts"

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    time_taken = db.Column(db.Integer, default=0)
    attempted_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "score": self.score,
            "total_questions": self.total_questions,
            "percentage": self.percentage,
            "time_taken": self.time_taken,
            "user_id": self.user_id,
            "quiz_id": self.quiz_id,
            "attempted_at": self.attempted_at
        }
