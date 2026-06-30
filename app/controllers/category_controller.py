from flask import request, jsonify
from app.extensions import db
from app.models.category_model import Category


def list_categories():
    categories = Category.query.all()
    return jsonify([c.to_dict() for c in categories]), 200


def create_category():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    if not name:
        return jsonify({"error": "name is required"}), 400

    if Category.query.filter_by(name=name).first():
        return jsonify({"error": "Category already exists"}), 409

    category = Category(name=name, description=data.get("description", ""))
    db.session.add(category)
    db.session.commit()
    return jsonify(category.to_dict()), 201


def update_category(category_id):
    category = Category.query.get_or_404(category_id)
    data = request.get_json() or {}

    if "name" in data:
        name = data["name"].strip()
        existing = Category.query.filter_by(name=name).first()
        if existing and existing.id != category.id:
            return jsonify({"error": "Category name already exists"}), 409
        category.name = name
    if "description" in data:
        category.description = data["description"]

    db.session.commit()
    return jsonify(category.to_dict()), 200


def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted"}), 200
