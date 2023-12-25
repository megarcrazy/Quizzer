from app import app


# def insert_sample_quizzes():
#     """Insert sample quiz values for testing."""
#     if not app.model.Quiz.query.first():
#         quiz1 = app.model.Quiz(quiz_id='EWIOFRJ9', name='Math')
#         quiz2 = app.model.Quiz(quiz_id='9E3FEJA', name='Dog Trivia')
#         db.session.add(quiz1)
#         db.session.add(quiz2)
#         db.session.commit()


if __name__ == '__main__':
    # # Insert sample values to the testing SQLite database
    # insert_sample_quizzes()

    # Run the Flask backend application
    app.run(debug=True)
