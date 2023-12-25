from flask import jsonify
from app import app
from app.models import Quiz


@app.route('/quiz', methods=['GET'])
def get_users():
    """Get all quiz data."""
    quizzes = Quiz.query.all()
    user_list = [
        {'id': quiz.id, 'name': quiz.name}
        for quiz in quizzes
    ]
    return jsonify({'quizzes': user_list})
