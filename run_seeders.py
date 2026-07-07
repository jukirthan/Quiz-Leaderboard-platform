from dotenv import load_dotenv

load_dotenv()

from app import create_app

from app.seeders.admin_seeder import seed_admin

app = create_app()

with app.app_context():
    seed_admin()
