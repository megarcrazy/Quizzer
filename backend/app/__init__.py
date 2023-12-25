from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

# Setup testing environment for application and database
if Config.TESTING_ENVIRONMENT:
    from .setup_test_db import create_db, insert_sample_quizzes

    with app.app_context():
        # Create testing database
        create_db(db)

        # Insert sample values to the database
        insert_sample_quizzes(db)

# Import routes to access the Flask application routes
from app import routes  # noqa: E402, F401
