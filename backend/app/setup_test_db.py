from flask_sqlalchemy.extension import SQLAlchemy
from app.models import Quiz, QuizQuestion, QuizOption


def insert_sample_data(db: SQLAlchemy) -> None:
    _insert_sample_quizzes(db)
    _insert_sample_questions(db)
    _insert_sample_options(db)


def _insert_sample_quizzes(db: SQLAlchemy) -> None:
    """Insert sample quiz values for testing."""
    data_list = [
        {'name': 'Math', 'code': 'ASDASDAA'},
        {'name': 'Science', 'code': 'FGFGFGFG'}
    ]
    for data in data_list:
        row = Quiz(
            name=data['name'],
            code=data['code']
        )
        db.session.add(row)
    db.session.commit()


def _insert_sample_questions(db: SQLAlchemy) -> None:
    """Insert sample questions for testing."""
    data_list = [
        {'quiz_id': '1', 'text': 'Evaluate 1 + 1'},
        {'quiz_id': '1', 'text': 'Find the derivative of x^2 in terms of x'},
        {'quiz_id': '2', 'text': 'What is the unit of power?'},
        {'quiz_id': '2', 'text': 'Why did the chicken cross the road?'},
    ]
    for data in data_list:
        row = QuizQuestion(
            quiz_id=data['quiz_id'],
            text=data['text']
        )
        db.session.add(row)
    db.session.commit()


def _insert_sample_options(db: SQLAlchemy) -> None:
    """Insert sample questions for testing."""
    data_list = [
        {'question_id': '1', 'text': 'Window'},
        {'question_id': '2', 'text': '2'},
        {'question_id': '3', 'text': '2x'},
        {'question_id': '4', 'text': 'x^3/3'},
        {'question_id': '5', 'text': 'What?'},
        {'question_id': '6', 'text': 'Watt'},
        {'question_id': '7', 'text': 'To get to the other side'},
        {'question_id': '8', 'text': 'No'},
    ]
    for data in data_list:
        row = QuizOption(
            question_id=data['question_id'],
            text=data['text']
        )
        db.session.add(row)
    db.session.commit()
