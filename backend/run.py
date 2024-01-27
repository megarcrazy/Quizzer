from app import create_app
from config import Config


if __name__ == '__main__':
    # Grab config variables
    database_url = Config.SQLALCHEMY_DATABASE_URI
    toggle_new_database = Config.NEW_ENVIRONMENT
    # Run the Flask backend application
    app = create_app(database_url, toggle_new_database)
    app.run(debug=True)
