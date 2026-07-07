from datetime import timedelta
import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()


def _database_uri():
    url = os.getenv("DATABASE_URL") or os.getenv("MYSQL_URL")
    if url:
        if url.startswith("mysql://"):
            return url.replace("mysql://", "mysql+pymysql://", 1)
        return url

    user = os.getenv("MYSQLUSER") or os.getenv("DB_USER", "root")
    password = os.getenv("MYSQLPASSWORD") or os.getenv("DB_PASSWORD", "root123")
    host = os.getenv("MYSQLHOST") or os.getenv("DB_HOST", "localhost")
    port = os.getenv("MYSQLPORT", "3306")
    name = os.getenv("MYSQLDATABASE") or os.getenv("DB_NAME", "quiz_app")

    return (
        f"mysql+pymysql://{quote_plus(user)}:{quote_plus(password)}"
        f"@{host}:{port}/{name}"
    )


class Config:
    SQLALCHEMY_DATABASE_URI = _database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-key-change-me")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_MINUTES", "15"))
    )