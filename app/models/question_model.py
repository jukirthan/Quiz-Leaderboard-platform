from app.extensions import db
import enum


class AnswerEnum(str, enum.Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(500), nullable=False)
    option_b = db.Column(db.String(500), nullable=False)
    option_c = db.Column(db.String(500), nullable=False)
    option_d = db.Column(db.String(500), nullable=False)
    correct_answer = db.Column(db.Enum(AnswerEnum), nullable=False)
    marks = db.Column(db.Integer, default=1, nullable=False)

    quiz = db.relationship("Quiz", back_populates="questions")

    def to_dict(self, include_answer=False):
        data = {
            "id": self.id,
            "quiz_id": self.quiz_id,
            "question_text": self.question_text,
            "option_a": self.option_a,
            "option_b": self.option_b,
            "option_c": self.option_c,
            "option_d": self.option_d,
            "marks": self.marks,
        }
        if include_answer:
            data["correct_answer"] = self.correct_answer.value
        return data

    def options_for_play(self):
        return [
            {"key": "A", "text": self.option_a},
            {"key": "B", "text": self.option_b},
            {"key": "C", "text": self.option_c},
            {"key": "D", "text": self.option_d},
        ]
