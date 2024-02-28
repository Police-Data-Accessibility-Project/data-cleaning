# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Initialize the SQLAlchemy object here

class DataEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    column_a = db.Column(db.String(50), nullable=False)
    original_column_b = db.Column(db.String(50), nullable=False)
    proposed_column_c_change = db.Column(db.String(50), nullable=False)
    reviewed = db.Column(db.Boolean, default=False, nullable=False)