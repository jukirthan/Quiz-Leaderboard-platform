from app.extensions import db
from app.models.category import Category


def seed_categories():
    if Category.query.count() > 0:
        return

    categories = [
        Category(name="Science", description="Physics, chemistry, biology and more"),
        Category(name="History", description="World history and events"),
        Category(name="Technology", description="Computers, software and gadgets"),
        Category(name="Mathematics", description="Numbers, algebra and geometry"),
        Category(name="Geography", description="Countries, capitals and maps"),
        Category(name="Sports", description="Football, cricket, Olympics and more"),
        Category(name="Entertainment", description="Movies, music and pop culture"),
        Category(name="General Knowledge", description="A bit of everything"),
    ]
    for c in categories:
        db.session.add(c)
    db.session.commit()
    print(f"Seeded {len(categories)} categories")
