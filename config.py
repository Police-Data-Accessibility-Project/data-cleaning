from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data_correction.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'


def create_app():
    app = Flask(__name__,
                template_folder='app/templates',
                static_folder='app/static')
    app.config.from_object(Config)
    return app

