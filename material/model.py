from flask_sqlalchemy import SQLAlchemy
from config.setup import db

class Category(db.Model):
    __tablename__ = "app_category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'{self.name}'
    
class Unit(db.Model):
    __tablename__ = "app_unit"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'{self.name}'

class Material(db.Model):
    __tablename__ = "app_material"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('app_unit.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('app_category.id'), nullable=False)
    unit = db.relationship('Unit', backref=db.backref('materials', lazy=True))
    category = db.relationship('Category', backref=db.backref('materials', lazy=True))

    def __init__(self, description, cost, unit_id, category_id):
        self.description = description
        self.cost = cost
        self.unit_id = unit_id
        self.category_id = category_id

    def __repr__(self):
        return f'{self.description}'