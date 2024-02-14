import logging
from typing import Optional
from flask import Blueprint, jsonify, Response, request
from app import Quiz, QuizQuestion, QuizOption, sql_functions

app = Blueprint('app', __name__)

# ------------------------------
# Debug methods
# ------------------------------


@app.route('/debug-quiz', methods=['GET'])
def debug_get_quizzes() -> Response:
    """Get all quiz data."""
    try:
        response = sql_functions.fetch_table_data(Quiz)
        return jsonify({'quizzes': response})
    except Exception as e:
        logging.critical(f'Error: {str(e)}')
        return jsonify({'error': 'An error occurred'}), 500


@app.route('/debug-quiz-question', methods=['GET'])
def debug_get_quiz_questions() -> Response:
    """Get all quiz question data."""
    try:
        response = sql_functions.fetch_table_data(QuizQuestion)
        return jsonify({'quiz_questions': response})
    except Exception as e:
        logging.critical(f'Error: {str(e)}')
        return jsonify({'error': 'An error occurred'}), 500


@app.route('/debug-quiz-option', methods=['GET'])
def debug_get_quiz_options() -> Response:
    """Get all quiz option data."""
    try:
        response = sql_functions.fetch_table_data(QuizOption)
        return jsonify({'quiz_options': response})
    except Exception as e:
        logging.critical(f'Error: {str(e)}')
        return jsonify({'error': 'An error occurred'}), 500


# ------------------------------
# Route methods
# ------------------------------


@app.route('/get-full-quiz/<quiz_id>', methods=['GET'])
def get_full_quiz(quiz_id: str) -> Response:
    """Get all full quiz data with quiz id filter."""
    try:
        data = sql_functions.select_full_quiz(quiz_id)
        return jsonify({'full_quiz': data})
    except Exception as e:
        logging.critical(f'Error: {str(e)}')
        return jsonify({'error': 'An error occurred'}), 500


@app.route('/save-quiz', methods=['POST'])
def save_quiz() -> Response:
    try:
        data = request.get_json()
        result = sql_functions.save_quiz(data)
        if result:
            message = 'Quiz saved successfully'
        else:
            message = 'Failed to save quiz'
        return jsonify({'message': message})
    except Exception as e:
        logging.critical(f'Error: {str(e)}')
        return jsonify({'error': 'An error occurred'}), 500


@app.route('/delete-quiz', methods=['POST'])
def delete_quiz() -> Response:
    try:
        data = request.get_json()
        result = sql_functions.delete_quiz(data)
        if result:
            message = 'Quiz deleted successfully'
        else:
            message = 'Failed to delete quiz'
        return jsonify({'message': message})
    except Exception as e:
        logging.critical(f'Error: {str(e)}')
        return jsonify({'error': 'An error occurred'}), 500


@app.route('/get-quiz/<limit>', methods=['GET'])
@app.route('/get-quiz', methods=['GET'])
def get_quizzes(limit: Optional[str] = '0') -> Response:
    """Get a list of quizzes from the database with amount up to the limit or
    0 for all.
    """
    try:
        try:
            int(limit)
        except ValueError:
            return jsonify({'message': 'limit needs to be an integer'})
        quiz_list = sql_functions.get_quiz_list(limit)
        return jsonify({'quiz_list': quiz_list})
    except Exception as e:
        logging.critical(f'Error: {str(e)}')
        return jsonify({'error': 'An error occurred'}), 500
