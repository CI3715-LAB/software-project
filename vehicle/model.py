from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from config.setup import db

class VehicleBrand(db.Model):
    __tablename__ = "app_vehicle_brand"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    vehicles = db.relationship('Vehicle', backref='brand', lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'{self.name}'

class VehicleModel(db.Model):
    __tablename__ = "app_vehicle_model"

    id = db.Column(db.Integer, primary_key=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('app_vehicle_brand.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False, unique=True)
    vehicles = db.relationship('Vehicle', backref='model', lazy=True)

    def __init__(self, name, brand_id):
        self.name = name
        self.brand_id = brand_id

    def __repr__(self):
        return f'{self.name}'

class VehicleColor(db.Model):
    __tablename__ = "app_vehicle_color"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    vehicles = db.relationship('Vehicle', backref='color', lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'{self.name}'


class Vehicle(db.Model):
    __tablename__ = "app_vehicle"

    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(100), nullable=False, unique=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('app_vehicle_brand.id'), nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey('app_vehicle_model.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    chasis_serial = db.Column(db.String(100), nullable=False, unique=True)
    motor_serial = db.Column(db.String(100), nullable=False, unique=True)
    color_id = db.Column(db.Integer, db.ForeignKey('app_vehicle_color.id'), nullable=False)
    problem = db.Column(db.String(1024), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('app_client.id'), nullable=False)
    projects = db.relationship('Project', backref='vehicle', lazy=True)

    def __init__(self, plate, brand, model, year, chasis_serial, motor_serial, color, problem, client_id):
        self.plate = plate
        self.brand_id = brand
        self.model_id = model
        self.year = year
        self.chasis_serial = chasis_serial
        self.motor_serial = motor_serial
        self.color_id = color
        self.problem = problem
        self.client_id = client_id

    def __repr__(self):
        return f'{self.plate}'