# Raw SQL demonstration
import logging
from flask_sqlalchemy.extension import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


def create_new_tables_and_views(db: SQLAlchemy) -> None:
    """Generate all SQL table views if they do not exist.

    Parameters:
        - db (flask_sqlalchemy.extension.SQLAlchemy): SQL database to execute
            the query.
    """
    _drop_existing_tables_and_views(db)
    _create_quiz_table(db)
    _create_quiz_question_table(db)
    _create_quiz_option_table(db)
    _create_full_quiz_view(db)


def _execute_query(db: SQLAlchemy, query: str) -> None:
    """Execute query with try catch and commit SQL changes."""
    try:
        db.session.execute(text(query))
        db.session.commit()
    except SQLAlchemyError as e:
        logging.critical(f"Failed to execute query: {query}")
        logging.debug(e)


def _drop_existing_tables_and_views(db: SQLAlchemy) -> None:
    """Drop all existing tables and views in the database."""
    # Drop all tables
    table_list = ['Quiz', 'QuizQuestion', 'QuizOption']
    for table in table_list:
        query = f'DROP TABLE IF EXISTS {table};'
        _execute_query(db, query)

    # Drop all views
    view_list = ['viewFullQuiz']
    for view in view_list:
        query = f'DROP VIEW IF EXISTS {view};'
        _execute_query(db, query)


def _create_quiz_table(db: SQLAlchemy) -> None:
    """Generate the quiz table."""
    query = """
    CREATE TABLE IF NOT EXISTS Quiz (
        quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        code TEXT NOT NULL UNIQUE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """
    _execute_query(db, query)


def _create_quiz_question_table(db: SQLAlchemy) -> None:
    """Generate the quiz table."""
    query = """
    CREATE TABLE IF NOT EXISTS QuizQuestion (
        question_id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_id INTEGER,
        text TEXT,
        FOREIGN KEY (quiz_id) REFERENCES Quiz (quiz_id)
    )
    """
    _execute_query(db, query)


def _create_quiz_option_table(db: SQLAlchemy) -> None:
    """Generate the quiz table."""
    query = """
    CREATE TABLE IF NOT EXISTS QuizOption (
        option_id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER,
        text TEXT,
        FOREIGN KEY (question_id) REFERENCES QuizQuestion (question_id)
    )
    """
    _execute_query(db, query)


def _create_full_quiz_view(db: SQLAlchemy) -> None:
    """Generate the full quiz view containing the tables Quiz, QuizQuestion
    and QuizOption.
    """
    query = """
    CREATE VIEW IF NOT EXISTS viewFullQuiz AS
    SELECT
        Quiz.quiz_id AS quiz_id,
        Quiz.name AS name,
        Quiz.code AS code,
        Quiz.created_at AS created_at,
        Quiz.updated_at AS updated_at,
        QuizQuestion.text AS question_text,
        QuizOption.text AS option_text
    FROM Quiz
    INNER JOIN QuizQuestion
    ON Quiz.quiz_id = QuizQuestion.quiz_id
    INNER JOIN QuizOption
    ON QuizQuestion.question_id = QuizOption.option_id
    """
    _execute_query(db, query)
