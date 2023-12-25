from app import app


if __name__ == '__main__':
    # # Insert sample values to the testing SQLite database
    # insert_sample_quizzes()

    # Run the Flask backend application
    app.run(debug=True)
