from flask import jsonify
from app import app
from app.models import Quiz


@app.route('/quiz', methods=['GET'])
def get_users():
    """Get all quiz data."""
    quizzes = Quiz.query.all()
    quiz_list = [
        {
            'id': quiz.id,
            'name': quiz.name,
            'code': quiz.code,
            'created_at': quiz.created_at,
            'updated_at': quiz.updated_at
        }
        for quiz in quizzes
    ]
    return jsonify({'quizzes': quiz_list})
