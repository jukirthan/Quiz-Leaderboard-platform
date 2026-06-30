from app.extensions import db
from datetime import datetime


class Quiz(db.Model):
    __tablename__ = "quizzes"

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    is_public = db.Column(db.Boolean, default=False, nullable=False)
    time_limit = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    creator = db.relationship("User", back_populates="quizzes")
    category = db.relationship("Category", back_populates="quizzes")
    questions = db.relationship("Question", back_populates="quiz", cascade="all, delete-orphan")
    attempts = db.relationship("QuizAttempt", back_populates="quiz", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "creator_id": self.creator_id,
            "creator_username": self.creator.username if self.creator else None,
            "category_id": self.category_id,
            "category_name": self.category.name if self.category else None,
            "title": self.title,
            "description": self.description,
            "is_public": self.is_public,
            "time_limit": self.time_limit,
            "question_count": len(self.questions),
            "total_marks": sum(q.marks for q in self.questions),
            "created_at": self.created_at.isoformat(),
        }

    def to_dict_with_questions(self, include_answers=False):
        data = self.to_dict()
        data["questions"] = [
            q.to_dict(include_answer=include_answers) for q in self.questions
        ]
        return data
