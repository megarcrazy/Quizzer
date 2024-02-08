from flask_sqlalchemy.extension import SQLAlchemy
from app.models import Quiz, QuizQuestion, QuizOption


def insert_sample_data(db: SQLAlchemy) -> None:
    _insert_sample_quizzes(db)
    _insert_sample_questions(db)
    _insert_sample_options(db)


def _insert_sample_quizzes(db: SQLAlchemy) -> None:
    """Insert sample quiz values for testing."""
    data_list = [
        {'name': 'Math'},
        {'name': 'Science'}
    ]
    for data in data_list:
        row = Quiz(name=data['name'])
        db.session.add(row)
    db.session.commit()


def _insert_sample_questions(db: SQLAlchemy) -> None:
    """Insert sample questions for testing."""
    data_list = [
        {'quiz_id': '1', 'text': 'Evaluate 1 + 1', 'question_number': 1},
        {'quiz_id': '1', 'text': 'Find the derivative of x^2 in terms of x',
         'question_number': 2},
        {'quiz_id': '2', 'text': 'What is the unit of power?',
         'question_number': 3},
        {'quiz_id': '2', 'text': 'Why did the chicken cross the road?',
         'question_number': 4},
    ]
    for data in data_list:
        row = QuizQuestion(**data)
        db.session.add(row)
    db.session.commit()


def _insert_sample_options(db: SQLAlchemy) -> None:
    """Insert sample questions for testing."""
    data_list = [
        {'question_id': '1', 'text': 'Window', 'option_number': 1},
        {'question_id': '1', 'text': '2', 'option_number': 2},
        {'question_id': '2', 'text': '2x', 'option_number': 1},
        {'question_id': '2', 'text': 'x^3/3', 'option_number': 2},
        {'question_id': '3', 'text': 'What?', 'option_number': 1},
        {'question_id': '3', 'text': 'Watt', 'option_number': 2},
        {'question_id': '4', 'text': 'To get to the other side',
         'option_number': 1},
        {'question_id': '4', 'text': 'No', 'option_number': 2},
    ]
    for data in data_list:
        row = QuizOption(**data)
        db.session.add(row)
    db.session.commit()
