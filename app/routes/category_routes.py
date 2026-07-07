from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models.category import Category
from app.utils import success_response, error_response

category_bp = Blueprint("category_bp", __name__)


@category_bp.route("/", methods=["GET"])
def get_categories():
    categories = Category.query.all()
    return success_response("Categories fetched", [c.to_dict() for c in categories])


@category_bp.route("/", methods=["POST"])
@jwt_required()
def create_category():
    data = request.get_json()
    name = data.get("name")

    if not name:
        return error_response("name is required")

    if Category.query.filter_by(name=name).first():
        return error_response("Category already exists")

    category = Category(name=name)
    db.session.add(category)
    db.session.commit()

    return success_response("Category created successfully", category.to_dict(), 201)