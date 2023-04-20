from flask_sqlalchemy import SQLAlchemy
from config.setup import db

class Activity(db.Model):
    __tablename__ = "app_activity"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    action_id = db.Column(db.Integer, db.ForeignKey('app_action.id'), nullable=False)
    action = db.relationship('Action', backref='activity', lazy=True, foreign_keys=[action_id])

    def __init__(self, name, action_id):
        self.name = name
        self.action_id = action_id

    def __repr__(self):
        return f'{self.name}'
    
class Action(db.Model):
    __tablename__ = "app_action"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('app_plan.id'), nullable=False)
    plan = db.relationship('Plan', backref='action', lazy=True, foreign_keys=[plan_id])

    def __init__(self, name, plan_id):
        self.name = name
        self.plan_id = plan_id

    def __repr__(self):
        return f'{self.name}'

class Plan(db.Model):
    __tablename__ = "app_plan"

    # Base
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    hours = db.Column(db.Integer, nullable=True)
    amount = db.Column(db.Float, nullable=True)

    responsible_id = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)
    responsible = db.relationship('User', backref='plan', lazy=True, foreign_keys=[responsible_id])

    project_id = db.Column(db.Integer, db.ForeignKey('app_project.id'), nullable=False)
    project = db.relationship('Project', backref='plan', lazy=True, foreign_keys=[project_id])

    # Human Resources
    personnel_count = db.Column(db.Integer, nullable=True)
    personnel_hours = db.Column(db.Integer, nullable=True)
    personnel_cost = db.Column(db.Float, nullable=True)
    personnel_amount = db.Column(db.Float, nullable=True)
    
    # Materials
    material_id = db.Column(db.Integer, db.ForeignKey('app_material.id'), nullable=True)
    material_count = db.Column(db.Integer, nullable=True)
    material_cost = db.Column(db.Float, nullable=True)
    material_amount = db.Column(db.Float, nullable=True)

    #action_id = db.Column(db.Integer, db.ForeignKey('app_action.id'), nullable=True)
    #action = db.relationship('Action', backref='plan', lazy=True, foreign_keys=[action_id])

    #activity_id = db.Column(db.Integer, db.ForeignKey('app_activity.id'), nullable=True)
    #activity = db.relationship('Activity', backref='plan', lazy=True, foreign_keys=[activity_id])

    def __init__(self, start_date, end_date, hours, amount, responsible_id, project_id, personnel_count,
                  personnel_amount, personnel_cost, personnel_hours, material_id, material_amount, material_cost, material_count):
        self.start_date = start_date
        self.end_date = end_date
        self.hours = hours
        self.amount = amount
        self.responsible_id = responsible_id
        self.project_id = project_id

        self.personnel_count = personnel_count
        self.personnel_amount = personnel_amount
        self.personnel_cost = personnel_cost
        self.personnel_hours = personnel_hours

        self.material_id = material_id
        self.material_amount = material_amount
        self.material_cost = material_cost
        self.material_count = material_count

        #self.action_id = action_id
        #self.activity_id = activity_id

    def __repr__(self):
        return f'Plan {self.project}'