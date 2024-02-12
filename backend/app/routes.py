import logging
from flask import Blueprint, jsonify, Response, request
from app import Quiz, QuizQuestion, QuizOption, sql_functions

app = Blueprint('app', __name__)

# ------------------------------
# Debug methods
# ------------------------------


@app.route('/debug-quiz', methods=['GET'])
def get_quizzes() -> Response:
    """Get all quiz data."""
    try:
        response = sql_functions.fetch_table_data(Quiz)
        return jsonify({'quizzes': response})
    except Exception as e:
        logging.critical(f'Error: {str(e)}')
        return jsonify({'error': 'An error occurred'}), 500


@app.route('/debug-quiz-question', methods=['GET'])
def get_quiz_questions() -> Response:
    """Get all quiz question data."""
    try:
        response = sql_functions.fetch_table_data(QuizQuestion)
        return jsonify({'quiz_questions': response})
    except Exception as e:
        logging.critical(f'Error: {str(e)}')
        return jsonify({'error': 'An error occurred'}), 500


@app.route('/debug-quiz-option', methods=['GET'])
def get_quiz_options() -> Response:
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


@app.route('/delete-quiz/<quiz_id>', methods=['POST'])
def delete_quiz(quiz_id: str) -> Response:
    try:
        quiz_id = int(quiz_id)
        result = sql_functions.delete_quiz(quiz_id)
        if result:
            message = 'Quizz(es) deleted successfully'
        else:
            message = 'Failed to delete'
        return jsonify({'message': message})
    except ValueError as e:
        logging.critical(f'Error: {str(e)}')
        return jsonify({'error': 'quiz_id must be an integer'}), 500
    except Exception as e:
        logging.critical(f'Error: {str(e)}')
        return jsonify({'error': 'An error occurred'}), 500
