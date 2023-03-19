from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from config.setup import db

class Client(db.Model):
    __tablename__ = "app_client"

    id = db.Column(db.Integer, primary_key=True)
    ci = db.Column(db.String(100), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date)
    contact_number = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    vehicles = db.relationship('Vehicle', cascade="all,delete", backref='client', lazy=True)

    def __init__(self, ci, name, lastname, birth_date, contact_number, email, address):
        self.ci = ci
        self.name = name
        self.lastname = lastname
        self.birth_date = birth_date
        self.contact_number = contact_number
        self.email = email
        self.address = address

    def __repr__(self):
        return f'{self.ci}'