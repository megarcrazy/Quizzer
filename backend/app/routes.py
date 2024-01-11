from typing import Dict, List
from flask import jsonify
from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy.exc import SQLAlchemyError
from app import app, db, Quiz, QuizQuestion, QuizOption, sql_functions

# Routes for testing and debugging the database


def _fetch_table_data(table: DefaultMeta) -> List[Dict[str, str]]:
    """Dynamically fetch all of table data from SQL and return json list."""
    data_list = table.query.all()

    # Fetch column names dynamically from the model
    columns = [column.key for column in table.__table__.columns]

    # Convert the query result to a list of dictionaries
    response = [
        {column: getattr(data, column) for column in columns}
        for data in data_list
    ]
    return response


@app.route('/debug-quiz', methods=['GET'])
def get_quizzes():
    """Get all quiz data."""
    try:
        response = _fetch_table_data(Quiz)
        return jsonify({'quizzes': response})
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500


@app.route('/debug-quiz-question', methods=['GET'])
def get_quiz_questions():
    """Get all quiz question data."""
    try:
        response = _fetch_table_data(QuizQuestion)
        return jsonify({'quiz_questions': response})
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500


@app.route('/debug-quiz-option', methods=['GET'])
def get_quiz_options():
    """Get all quiz option data."""
    try:
        response = _fetch_table_data(QuizOption)
        return jsonify({'quiz_options': response})
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500


@app.route('/debug-full-quiz', methods=['GET'])
def get_fullquiz():
    """Get all full quiz data."""
    try:
        cursor_result = sql_functions.select_full_quiz(db)
        rows = cursor_result.fetchall()  # Get all table rows
        keys = cursor_result.keys()  # Get table columns
        # Generate dictionary using keys and rows of data
        response = [dict(zip(keys, row)) for row in rows]
        return jsonify({'full_quiz': response})
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500
