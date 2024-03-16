import os

from flask import Flask


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data_correction.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'


def create_app():
    app = Flask(__name__,
                template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
                static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    # Load configuration variables into Flask application
    app.config.from_object(Config)
    return app

