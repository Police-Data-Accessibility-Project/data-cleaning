import os

from flask import Flask


class Config:
    # Get path from current working directory to the database file
    DATABASE_PATH = os.path.join(os.getcwd(), 'instance', 'data_correction.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'


def create_app():
    app = Flask(__name__,
                template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
                static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    # Load configuration variables into Flask application
    app.config.from_object(Config)

    # Check if the database file exists (the [10:] is to remove the 'sqlite:///' prefix)
    database_path = app.config['SQLALCHEMY_DATABASE_URI'][10:]
    if not os.path.exists(database_path):
        raise FileNotFoundError(f"No database file found at {database_path}"
                                f"Ensure database file is created "
                                f"and app is run from proper working directory at root of project")
    else:
        print(f"Database file found at {database_path}")
    return app

