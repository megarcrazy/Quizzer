from datetime import datetime
from typing import Any, Dict, Generator, List, Optional
from contextlib import contextmanager
import logging
from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import and_
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
                Quiz.created_at,
                Quiz.updated_at,
                QuizQuestion.question_id,
                QuizQuestion.question_number,
                QuizQuestion.text.label('question_text'),
                QuizOption.option_id,
                QuizOption.option_number,
                QuizOption.text.label('option_text'),
                QuizOption.correct_answer
            )
            .join(QuizQuestion, QuizQuestion.quiz_id == Quiz.quiz_id)
            .join(QuizOption,
                  QuizOption.question_id == QuizQuestion.question_id)
            .filter(Quiz.quiz_id == quiz_id)
        )

        query_result = query.all()

    json_dict_list = _sql_row_to_dict_list(query_result)
    return json_dict_list


def delete_quiz(delete_quiz_data: Dict[str, str]) -> bool:
    """Delete quiz by quiz ID in the database.

    Parameters:

    delete_quiz_data (Dict[str, str]): Dictionary contain the quiz id to
        delete quiz.

    Returns:
        bool: True if a quiz got deleted else False.
    """
    quiz_id = int(delete_quiz_data['quiz_id'])

    with _get_session(True, True) as session:
        # Filter by condition and delete
        rows_deleted = session.query(Quiz).filter(quiz_id == quiz_id).delete()

        # Commit session
        session.commit()

    # Return False if no rows deleted
    if rows_deleted == 0:
        return False
    return True


def save_quiz(question_data: Dict[str, Any]) -> bool:
    """
    Update quiz details, questions, and options.

    Args:
        data (Dict[str, Any]): Nested dictionary containing data for quiz,
            quiz questions and quiz question optinos.
            'data' exists in the format:
            data = {
                'quiz_data': {
                    'quiz_id': int,
                    'name': str,
                    'quiz_question_data': [
                        {
                            'question_number': int,
                            'text': str,
                            'quiz_option_data': [
                                {
                                    'option_number': int,
                                    'text': str,
                                    'correct_answer': bool
                                }
                            ]
                        }...
                    ]
                }
            }
    """
    # Use session to make changes in the database
    successfully_commited = False
    with _get_session(True, True) as session:
        # Get quiz data
        quiz_data = question_data['quiz_data']

        # Save quiz details
        quiz_id = _save_quiz_row(session, quiz_data)

        if quiz_id == 0:
            # Return early if no quiz was updated
            return False

        # Extract question data
        question_data_list = quiz_data['quiz_question_data']

        for question_data in question_data_list:
            # Save quiz question details
            question_id = _save_question_row(session, question_data, quiz_id)

            # Extract option data
            option_data_list = question_data['quiz_option_data']

            for option_data in option_data_list:
                # Save quiz option details
                _save_option_rows(session, option_data, question_id)

            # Get highest option number and delete all the options with higher
            # option numbers
            threshold = _get_max_quiz_number_threshold(option_data_list,
                                                       'option_number')
            _delete_rest_of_rows(session, QuizOption, 'question_id',
                                 question_id, 'option_number', threshold)

        # Get highest question number and delete all the questions with higher
        # question numbers
        threshold = _get_max_quiz_number_threshold(question_data_list,
                                                   'question_number')
        _delete_rest_of_rows(session, QuizQuestion, 'quiz_id', quiz_id,
                             'question_number', threshold)

        # Flag commits were successful
        successfully_commited = True

    return successfully_commited


def get_quiz_list(limit: int) -> List[Dict[str, str]]:
    """Extract a list of quiz with list size up to the limit.

    Parameters:
        limit (int): Quiz list size limit or 0 for all.

    Returns:
        List[Quiz]: List of quizzess from the database.
    """
    with _get_session(False, False) as session:
        if limit == 0:
            quiz_list = session.query(Quiz).all()
        else:
            quiz_list = session.query(Quiz).limit(limit).all()

    # Convert quiz list to list of dictionaries
    json_quiz_list = []
    for quiz in quiz_list:
        data = {
            'quiz_id': quiz.quiz_id,
            'name': quiz.name
        }
        json_quiz_list.append(data)

    return json_quiz_list


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


def _row_exist(session: Session, table: DefaultMeta, filters: Dict[str, Any]
               ) -> Optional[Row]:
    """Check if data exists after filtering a table."""
    data = session.query(table).filter_by(**filters).first()
    if data:
        # Return data if at least one row found
        return data
    # Return None if no rows found
    return None


def _insert_row(session: Session, table: DefaultMeta, values: Dict[str, Any]
                ) -> Row:
    """Insert row into SQL table with new values."""
    new_row = table(**values)

    # Append new row
    session.add(new_row)

    return new_row


def _update_row(session: Session, table: DefaultMeta, filters: Dict[str, Any],
                values: Dict[str, Any]) -> bool:
    """Update row in SQL with filters and new values."""
    updated_rows = session.query(table).filter_by(**filters).update(values)
    # Return False if no rows updated
    if updated_rows == 0:
        return False
    return True


def _save_quiz_row(session: Session, quiz_data: Dict[str, Any]) -> int:
    """Save quiz row and return quiz ID."""
    quiz_id = quiz_data.get('quiz_id', 0)
    quiz_name = quiz_data['name']
    if quiz_id == 0:
        # If the given quiz ID is 0, create new quiz
        values = {Quiz.name.name: quiz_name}
        quiz = _insert_row(session, Quiz, values)
    else:
        # Update quiz for given quiz ID
        filters = {Quiz.quiz_id.name: quiz_id}
        values = {
            Quiz.name.name: quiz_name,
            Quiz.updated_at.name: datetime.now()
        }
        updated = _update_row(session, Quiz, filters, values)
        if updated == 0:
            # Return 0 if no quiz was updated
            return 0

    # Commit and get quiz ID
    session.commit()
    if quiz_id == 0:
        quiz_id = quiz.quiz_id
    return quiz_id


def _save_question_row(session: Session, question_data: Dict[str, Any],
                       quiz_id: int) -> int:
    """Save question row and return question ID dictionary."""
    # Extract data from dictionary
    question_number = question_data['question_number']
    text = question_data['text']

    # Check if question number index already has a question
    exist_filters = {
        QuizQuestion.quiz_id.name: quiz_id,
        QuizQuestion.question_number.name: question_number
    }
    question = _row_exist(session, QuizQuestion, exist_filters)

    # Add new SQL row if the question number does not exist
    if question is None:
        # Add new question
        values = {
            QuizQuestion.quiz_id.name: quiz_id,
            QuizQuestion.question_number.name: question_number,
            QuizQuestion.text.name: text
        }
        question = _insert_row(session, QuizQuestion, values)
    else:
        # Update quiz question for given quiz ID
        filters = {
            QuizQuestion.quiz_id.name: quiz_id,
            QuizQuestion.question_number.name: question_number
        }
        values = {QuizQuestion.text.name: text}
        _update_row(session, QuizQuestion, filters, values)

    # Commit and get question ID
    session.commit()
    question_id = question.question_id
    return question_id


def _save_option_rows(session: Session, option_data: Dict[str, Any],
                      question_id: int) -> None:
    """Save option row."""
    # Extract data from dictionary
    option_number = option_data['question_number']
    text = option_data['text']
    correct_answer = option_data['correct_answer']

    # Check if question number index already has a question
    filters = {
        QuizOption.question_id.name: question_id,
        QuizOption.option_number.name: option_number
    }
    option = _row_exist(session, QuizOption, filters)

    # Add new SQL row if the option number does not exist
    if option is None:
        # Add new option
        values = {
            QuizOption.question_id.name: question_id,
            QuizOption.option_number.name: option_number,
            QuizOption.text.name: text,
            QuizOption.correct_answer.name: correct_answer
        }
        option = _insert_row(session, QuizOption, values)
    else:
        # Update quiz question for given quiz ID
        filters = {
            QuizOption.question_id.name: question_id,
            QuizOption.option_number.name: option_number,
            QuizOption.correct_answer.name: correct_answer
        }
        values = {QuizOption.text.name: text}
        _update_row(session, QuizOption, filters, values)

    # Commit and get question ID
    session.commit()
    question_id = option.question_id
    return question_id


def _get_max_quiz_number_threshold(data_list: Dict[str, Any], index_key: str
                                   ) -> int:
    """Get highest index number of given data list."""
    threshold = 0
    if data_list != []:
        threshold = data_list[-1][index_key]

    return threshold


def _delete_rest_of_rows(session: Session, table: DefaultMeta,
                         foreign_key_name: str, foreign_key_value: int,
                         index_column_name: str, threshold: int) -> None:
    """Delete rows with custom index number above an integer threshold."""

    condition = and_(
        getattr(table, foreign_key_name) == foreign_key_value,
        getattr(table, index_column_name) > threshold
    )
    # Filter by condition and delete
    session.query(table).filter(condition).delete()

    # Commit session
    session.commit()
