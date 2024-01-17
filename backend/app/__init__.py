import logging
from flask import Flask
from .config import Config
from app.models import db, Quiz, QuizQuestion, QuizOption  # noqa: F401
import app.setup_test_db as setup_test_db
import app.sql_functions as sql_functions  # noqa: F401

# Set logger on debug level
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Initiate Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
db.init_app(app)

# Setup testing environment for application and database using sqlite
with app.app_context():
    if Config.NEW_ENVIRONMENT:
        db.drop_all()
        db.create_all()  # Create tables and views

        # Insert sample values to the database
        setup_test_db.insert_sample_data(db)
    else:
        db.create_all()

# Import routes to access the Flask application routes
from app import routes  # noqa: E402, F401
