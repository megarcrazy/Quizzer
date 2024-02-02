# ORM demonstration

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Quiz(db.Model):
    __tablename__ = 'Quiz'

    # Auto-incremented quiz id
    quiz_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Name of the quiz
    name = db.Column(db.String(20), nullable=False)

    # Random unique code generated for the quiz
    code = db.Column(db.String(8), nullable=False, unique=True)

    # Created date
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Cascading updated
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)


class QuizQuestion(db.Model):
    __tablename__ = 'QuizQuestion'

    # Auto-incremented quiz question id
    question_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Foreign key to quiz table
    quiz_id = db.Column(
        db.Integer, db.ForeignKey('Quiz.quiz_id'), nullable=False)

    # Question number to show position in quiz
    question_number = db.Column(db.Integer, nullable=False)

    # Text representation of question
    text = db.Column(db.String(100), nullable=False)


class QuizOption(db.Model):
    __tablename__ = 'QuizOption'

    # Auto-incremented quiz option id
    option_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Foreign key to quiz question table
    question_id = db.Column(
        db.Integer, db.ForeignKey('QuizQuestion.question_id'), nullable=False)

    # Question number to show position in question
    option_number = db.Column(db.Integer, nullable=False)

    # Text represention of quiz option
    text = db.Column(db.String(20), nullable=False)
