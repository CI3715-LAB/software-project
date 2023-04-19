from flask_sqlalchemy import SQLAlchemy
from config.setup import db

class Activity(db.Model):
    __tablename__ = "app_activity"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    action_id = db.Column(db.Integer, db.ForeignKey('app_action.id'), nullable=False)
    action = db.relationship('Action', backref=db.backref('activities', lazy=True))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'{self.name}'
    
class Action(db.Model):
    __tablename__ = "app_action"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('app_plan.id'), nullable=False)
    plan = db.relationship('Action', backref=db.backref('actions', lazy=True))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'{self.name}'

class Plan(db.Model):
    __tablename__ = "app_plan"

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    hours = db.Column(db.Integer, nullable=True)
    responsible = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=True)
    personnel = db.Column(db.Integer, nullable=True)

    def __init__(self, description, cost, unit_id, category_id):
        self.description = description
        self.cost = cost
        self.unit_id = unit_id
        self.category_id = category_id

    def __repr__(self):
        return f'{self.description}'