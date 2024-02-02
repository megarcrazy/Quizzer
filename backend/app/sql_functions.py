from typing import Any, Dict, Generator, List
from contextlib import contextmanager
import logging
from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy.engine.row import Row
from sqlalchemy.orm import Session
from app import db, Quiz, QuizQuestion, QuizOption


# ------------------------------
# Debug methods
# ------------------------------

def fetch_table_data(table: DefaultMeta) -> List[Dict[str, Any]]:
    """Dynamically fetch all of table data from SQL and return json list.

    Parameters:
        - table (DefaultMeta): Table to query all.

    Returns:
        List[Dict[str, Any]]: returns dictionary list representation of the
            table.
    """
    # Query all columns from table
    data_list = table.query.all()

    # Fetch column names dynamically from the model
    columns = [column.key for column in table.__table__.columns]

    # Convert the query result to a list of dictionaries
    response = [
        {column: getattr(data, column) for column in columns}
        for data in data_list
    ]
    return response


# ------------------------------
# Context manager
# ------------------------------

@contextmanager
def _get_session(commit_query: bool, raise_error: bool
                 ) -> Generator[Session, None, None]:
    """Session context manager with commit query toggle."""
    try:
        session = db.session
        yield session
    except Exception as e:
        logging.critical(f'Error: {str(e)}')
        # Rollback all commits if commit fails
        if commit_query:
            db.session.rollback()
        # Raise error to catch at the decorated function
        if raise_error:
            raise e


# ------------------------------
# SQL session methods
# ------------------------------

def select_full_quiz(quiz_id: str) -> List[Dict[str, Any]]:
    """Select full quiz view containing the tables Quiz, QuizQuestion
    and QuizOption.

    Parameters:
        - quiz_id (str): Quiz ID to filter results to grab specific quiz.

    Returns:
        List[Dict[str, Any]]: Returns dictionary list representation of the
            full quiz.
    """
    with _get_session(False, False) as session:
        query = (
            session.query(
                Quiz.quiz_id,
                Quiz.name,
                Quiz.code,
                Quiz.created_at,
                Quiz.updated_at,
                QuizQuestion.question_id,
                QuizQuestion.text.label('question_text'),
                QuizOption.option_id,
                QuizOption.text.label('option_text')
            )
            .join(QuizQuestion, QuizQuestion.quiz_id == Quiz.quiz_id)
            .join(QuizOption,
                  QuizOption.question_id == QuizQuestion.question_id)
            .filter(Quiz.quiz_id == quiz_id)
        )

        query_result = query.all()

    json_dict_list = _sql_row_to_dict_list(query_result)
    return json_dict_list


# ------------------------------
# Helper methods
# ------------------------------

def _sql_row_to_dict_list(query_result: List[Row]) -> List[Dict[str, Any]]:
    """Convert SQL query list of row result to json dictionary list."""
    json_dict_list = []
    # Iterate rows in query result and convert to dictionary using column name
    # as keys and cell values as data
    for row in query_result:
        row_dictionary = dict(row._mapping)
        json_dict_list.append(row_dictionary)
    return json_dict_list
