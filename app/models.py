# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Initialize the SQLAlchemy object here

class DataEntry(db.Model):
    __tablename__ = 'entries_to_validate'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    state = db.Column(db.String)
    old_url = db.Column(db.String)
    possible_correct_url = db.Column(db.String)
    reviewed = db.Column(db.Boolean, nullable=False)