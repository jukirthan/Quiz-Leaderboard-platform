from flask import Flask

from app.config import Config
from app.extensions import bcrypt, cors, db, jwt
from app.middleware import register_error_handlers
from app.routes import register_blueprints


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)

    register_blueprints(app)
    register_error_handlers(app)

    return app
