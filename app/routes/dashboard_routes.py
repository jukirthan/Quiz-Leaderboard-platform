from flask import Blueprint
from app.middleware import auth_required
from app.controllers import dashboard_controller

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard", methods=["GET"])
@auth_required
def dashboard():
    return dashboard_controller.dashboard()
