"""Database model for player"""
from app import DB


class Player(DB.Model):
    """Class of database model imported into app.py"""
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(80), unique=True, nullable=False)
    score = DB.Column(DB.Integer, unique=False, nullable=False)

    def __repr__(self):
        return self.username
