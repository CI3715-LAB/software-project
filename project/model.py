from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
 
from config.setup import db

class Project (db.Model):
	__tablename__ = "app_project"
    
	id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.String(100), nullable=False)
	open_date = db.Column(db.Date, default=datetime.utcnow)
	close_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
	enabled = db.Column(db.Boolean(), default=True)
	vehicle_id = db.Column(db.Integer, db.ForeignKey('app_vehicle.id'), nullable=False)
	department_id = db.Column(db.Integer, db.ForeignKey('app_department.id'), nullable=False)
	manager_id = db.Column(db.Integer, db.ForeignKey('app_user.id', use_alter=True), nullable=False)
	problem = db.Column(db.String(100), nullable=True)
	solution = db.Column(db.String(100), nullable=True)
	amount = db.Column(db.Float, nullable=True)
	observation = db.Column(db.String(100), nullable=True)
	
	# one to one relationship with vehicle
	vehicle = db.relationship('Vehicle', backref='project', lazy=True)
	# one to one relationship with user
	manager = db.relationship('User', backref='projects', lazy=True, foreign_keys=[manager_id])
		
	def __init__(self, description, open_date, close_date, enabled, vehicle_id, department_id, manager_id, problem, solution, amount, observation):
		self.description = description
		self.open_date = open_date
		self.close_date = close_date
		self.enabled = enabled
		self.vehicle_id = vehicle_id
		self.department_id = department_id
		self.manager_id = manager_id
		self.problem = problem
		self.solution = solution
		self.amount = amount
		self.observation = observation

	def __repr__(self):
		return self.description