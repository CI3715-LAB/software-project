from flask_sqlalchemy import SQLAlchemy
 
from config.setup import db

class Department(db.Model):
	__tablename__ = "app_department"
	
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	# one to many relationship with user
	users = db.relationship('User', backref='department', lazy=True)
	projects = db.relationship('Project', backref='project', lazy=True)

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return self.name