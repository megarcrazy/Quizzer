from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Regular SQL tables

db = SQLAlchemy()


class Quiz(db.Model):
    # Auto-incremented quiz id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Name of the quiz
    name = db.Column(db.String(20), nullable=False)

    # Random unique code generated for the quiz
    code = db.Column(db.String(8), nullable=False, unique=True)

    # Created date
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Cascading updated
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Table relationship to quiz question table
    quiz_questions = db.relationship(
        'QuizQuestion', backref='quiz_parent', lazy='dynamic',
        cascade='all, delete-orphan')


class QuizQuestion(db.Model):
    # Auto-incremented quiz question id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Foreign key to quiz table
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)

    # Text representation of question
    text = db.Column(db.String(100), nullable=False)

    # Table relationship to quiz option table
    quiz_options = db.relationship(
        'QuizOption', backref='question_parent', lazy='dynamic',
        cascade='all, delete-orphan')


class QuizOption(db.Model):
    # Auto-incremented quiz option id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Foreign key to quiz question table
    question_id = db.Column(
        db.Integer, db.ForeignKey('quiz_question.id'), nullable=False)

    # Text represention of quiz option
    text = db.Column(db.String(20), nullable=False)
