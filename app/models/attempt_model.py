from app.extensions import db
from datetime import datetime
from app.models.question_model import AnswerEnum


class QuizAttempt(db.Model):
    __tablename__ = "quiz_attempts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"), nullable=False)
    score = db.Column(db.Integer, default=0)
    total_marks = db.Column(db.Integer, default=0)
    percentage = db.Column(db.Numeric(5, 2), default=0)
    completed_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship("User", back_populates="attempts")
    quiz = db.relationship("Quiz", back_populates="attempts")
    answers = db.relationship("UserAnswer", back_populates="attempt", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "quiz_id": self.quiz_id,
            "quiz_title": self.quiz.title if self.quiz else None,
            "score": self.score,
            "total_marks": self.total_marks,
            "percentage": float(self.percentage) if self.percentage is not None else 0,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


class UserAnswer(db.Model):
    __tablename__ = "user_answers"

    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey("quiz_attempts.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    selected_answer = db.Column(db.Enum(AnswerEnum), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)

    attempt = db.relationship("QuizAttempt", back_populates="answers")
