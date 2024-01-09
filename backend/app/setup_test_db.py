import flask_sqlalchemy
from app.models import Quiz


def insert_sample_quizzes(db: flask_sqlalchemy.extension.SQLAlchemy) -> None:
    """Insert sample quiz values for testing."""
    quiz1 = Quiz(name='Math', code='ASDASDAA')
    quiz2 = Quiz(name='Science', code='FGFGFGFG')
    db.session.add(quiz1)
    db.session.add(quiz2)
    db.session.commit()
