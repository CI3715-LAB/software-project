from flask_sqlalchemy import SQLAlchemy
from config.setup import db

class Activity(db.Model):
    __tablename__ = "app_activity"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    action_id = db.Column(db.Integer, db.ForeignKey('app_action.id'), nullable=False)
    action = db.relationship('Action', backref='activity', lazy=True, foreign_keys=[action_id])

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'{self.name}'
    
class Action(db.Model):
    __tablename__ = "app_action"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('app_plan.id'), nullable=False)
    plan = db.relationship('Plan', backref='action', lazy=True, foreign_keys=[plan_id])

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
    amount = db.Column(db.Float, nullable=True)
    personnel = db.Column(db.Integer, nullable=True)

    responsible_id = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)
    responsible = db.relationship('User', backref='plan', lazy=True, foreign_keys=[responsible_id])

    project_id = db.Column(db.Integer, db.ForeignKey('app_project.id'), nullable=False)
    project = db.relationship('Project', backref='plan', lazy=True, foreign_keys=[project_id])

    def __init__(self, start_date, end_date, hours, responsible_id, amount, personnel, project_id):
        self.start_date = start_date
        self.end_date = end_date
        self.hours = hours
        self.responsible_id = responsible_id
        self.amount = amount
        self.personnel = personnel
        self.project_id = project_id

    def __repr__(self):
        return f'Plan {self.project}'