from app import db

# SQL tables


class Quiz(db.Model):
    """SQLAlchemy model class for representing a Quiz entity in the
    database.
    """
    id = db.Column(
        db.String(8), unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
