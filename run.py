from flask_cors import CORS

from app import create_app

app = create_app()
CORS(app)

def init_db():
    with app.app_context():
        from app.extensions import db
        from app.utils import ensure_role_column

        db.create_all()
        ensure_role_column(db)


try:
    init_db()
except Exception as exc:
    print(f"Database initialization skipped: {exc}", flush=True)

if __name__ == "__main__":
    app.run(debug=True, port=5000)