# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Initialize the SQLAlchemy object here

class DataEntry(db.Model):
    __tablename__ = 'agencies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255))
    old_url = db.Column(db.String(255))
    possible_correct_url = db.Column(db.String(255))
    airtable_uid = db.Column(db.String(255))
    submitted_name = db.Column(db.String(255))
    no_web_presence = db.Column(db.Boolean)
    rejection_reason = db.Column(db.String(255))
    approved = db.Column(db.Boolean)