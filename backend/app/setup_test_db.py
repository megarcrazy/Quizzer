import flask_sqlalchemy
from app.models import Quiz


def create_db(db: flask_sqlalchemy.extension.SQLAlchemy) -> None:
    """Create the testing database."""
    # The database will be created with SQLite for testing and simplicity
    # In production, the database is not overwritten
    db.create_all()


def insert_sample_quizzes(db: flask_sqlalchemy.extension.SQLAlchemy) -> None:
    """Insert sample quiz values for testing."""
    if not Quiz.query.first():
        quiz1 = Quiz(id='EWIOFRJ9', name='Math')
        quiz2 = Quiz(id='9E3FEJA', name='Dog Trivia')
        db.session.add(quiz1)
        db.session.add(quiz2)
        db.session.commit()
