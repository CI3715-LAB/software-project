from datetime import datetime

from config.setup import db

class User (db.Model):
    __tablename__ = "app_user"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    date_joined = db.Column(db.Date, default=datetime.utcnow)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return f'{self.email}'