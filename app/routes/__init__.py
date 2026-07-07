from app.routes.auth_routes import auth_bp
from app.routes.category_routes import category_bp
from app.routes.quiz_routes import quiz_bp
from app.routes.attempt_routes import attempt_bp
from app.routes.dashboard_routes import dashboard_bp
from app.routes.admin_routes import admin_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(category_bp, url_prefix="/api/categories")
    app.register_blueprint(quiz_bp, url_prefix="/api/quizzes")
    app.register_blueprint(attempt_bp, url_prefix="/api/quiz_attempts")
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

