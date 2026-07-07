from flask import request
from app.extensions import db
from app.models.category import Category
from app.utils import success_response, error_response


def get_categories():
    categories = Category.query.all()
    return success_response(
        "Categories fetched",
        [category.to_dict() for category in categories]
    )


def create_category():
    data = request.get_json()
    name = data.get("name")

    if not name:
        return error_response("Name is required")

    if Category.query.filter_by(name=name).first():
        return error_response("Category already exists")

    category = Category(name=name)

    db.session.add(category)
    db.session.commit()

    return success_response(
        "Category created successfully",
        category.to_dict(),
        201
    )