from flask import Blueprint
from app.middleware import admin_required
from app.controllers import category_controller

categories_bp = Blueprint("categories", __name__)


@categories_bp.route("/categories", methods=["GET"])
def list_categories():
    return category_controller.list_categories()


@categories_bp.route("/categories", methods=["POST"])
@admin_required
def create_category():
    return category_controller.create_category()


@categories_bp.route("/categories/<int:category_id>", methods=["PUT"])
@admin_required
def update_category(category_id):
    return category_controller.update_category(category_id)


@categories_bp.route("/categories/<int:category_id>", methods=["DELETE"])
@admin_required
def delete_category(category_id):
    return category_controller.delete_category(category_id)
