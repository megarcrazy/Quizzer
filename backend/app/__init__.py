import logging
from flask import Flask
from app.models import db, Quiz, QuizQuestion, QuizOption  # noqa: F401
import app.setup_test_db as setup_test_db
import app.sql_functions as sql_functions  # noqa: F401
# Import routes to access the Flask application routes
from app import routes  # noqa: F401

# Set logger on debug level
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def create_app(database_url: str, toggle_new_database: bool) -> None:
    """Create flask app object.

    Args:
        database_url (str): SQL database url to connect.
        toggle_new_database (bool): Will reset database with sample data when
            creating app if True.
    """
    # Initiate Flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    db.init_app(app)

    # Setup testing environment for application and database using sqlite
    with app.app_context():
        # Link ORM to database
        app.register_blueprint(routes.app)

        if toggle_new_database:
            db.drop_all()
            db.create_all()  # Create tables and views

            # Insert sample values to the database
            setup_test_db.insert_sample_data(db)
        else:
            db.create_all()
    return app
