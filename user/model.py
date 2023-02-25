from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
 
from config.setup import db

# Role model
class Role (db.Model):
    __tablename__ = "app_role"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    # one to many relationship with user
    users = db.relationship('User', backref='role', lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'{self.name}'

class User (db.Model):
    __tablename__ = "app_user"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    date_joined = db.Column(db.Date, default=datetime.utcnow)
    # foreign key to role
    role_id = db.Column(db.Integer, db.ForeignKey('app_role.id'), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)
     
    def check_password(self, password):
        return check_password_hash(self.password,password)

    def __init__(self, username, password, role_id):
        self.username = username
        self.set_password(password)
        self.role_id = role_id

    def __repr__(self):
        return f'{self.username}'

