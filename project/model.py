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
	# many to many relationship with user
	# users = db.relationship('User', secondary='app_user_project', backref='projects')
	users = db.relationship('User', backref='project', lazy=True)

	def __init__(self, description, open_date, close_date, enabled):
		self.description = description
		self.open_date = open_date
		self.close_date = close_date
		self.enabled = enabled

	def __repr__(self):
		return f'{self.description[:10]}'


class UserProject (db.Model):
	__tablename__ = "app_user_project"
	
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)
	project_id = db.Column(db.Integer, db.ForeignKey('app_project.id'), nullable=False)

	def __init__(self, user_id, project_id):
		self.user_id = user_id
		self.project_id = project_id

	def __repr__(self):
		return f'{self.user_id} - {self.project_id}'