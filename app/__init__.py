from flask import Flask
from config import Config
from app.extensions import db, jwt, bcrypt, cors


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    from app.models import User, Category, Quiz, Question, QuizAttempt, UserAnswer  # noqa: F401

    from app.routes.auth_routes import auth_bp
    from app.routes.quiz_routes import quizzes_bp
    from app.routes.category_routes import categories_bp
    from app.routes.question_routes import questions_bp
    from app.routes.attempt_routes import attempts_bp
    from app.routes.leaderboard_routes import leaderboard_bp
    from app.routes.dashboard_routes import dashboard_bp
    from app.routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(quizzes_bp, url_prefix="/api")
    app.register_blueprint(categories_bp, url_prefix="/api")
    app.register_blueprint(questions_bp, url_prefix="/api")
    app.register_blueprint(attempts_bp, url_prefix="/api")
    app.register_blueprint(leaderboard_bp, url_prefix="/api")
    app.register_blueprint(dashboard_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()

    return app
