from flask import Flask
from .config import Config
from app.models import db
import app.setup_test_db as setup_test_db


# Initiate Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
db.init_app(app)

# Setup testing environment for application and database using sqlite
with app.app_context():
    if Config.NEW_ENVIRONMENT:
        db.drop_all()  # Drop existing tables

        db.create_all()  # Create SQL tables

        # Insert sample values to the database
        setup_test_db.insert_sample_quizzes(db)
    else:
        # Create SQL tables
        db.create_all()


# Import routes to access the Flask application routes
from app import routes  # noqa: E402, F401
