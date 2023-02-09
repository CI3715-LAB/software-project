from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
 
from config.setup import db

class User (db.Model):
    __tablename__ = "app_user"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    date_joined = db.Column(db.Date, default=datetime.utcnow)
    admin = db.Column(db.Boolean(), default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)
     
    def check_password(self, password):
        return check_password_hash(self.password,password)

    def __init__(self, username, email, password, admin):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.admin = admin or False

    def __repr__(self):
        return f'{self.username} : {self.email}'