from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from config.setup import db

class Type(db.Model):
	__tablename__ = "app_type"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False, unique=True)

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return f'{self.name}'
	
class Module(db.Model):
	__tablename__ = "app_module"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False, unique=True)
	permissions = db.relationship('Permission', backref='module', lazy=True)

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return f'{self.name}'

class Log(db.Model):
	__tablename__ = "app_log"

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)
	# relationship to user
	user = db.relationship('User', backref=db.backref('logs', lazy=True))
	description = db.Column(db.String(100), nullable=False)
	date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
	time = db.Column(db.String(100), nullable=False)
	# foreign key to type
	type_id = db.Column(db.Integer, db.ForeignKey('app_type.id'), nullable=False)
	# relationship to type
	type = db.relationship('Type', backref=db.backref('logs', lazy=True))
	# foreign key to module
	module_id = db.Column(db.Integer, db.ForeignKey('app_module.id'), nullable=False)
	# relationship to module
	module = db.relationship('Module', backref=db.backref('logs', lazy=True))

	def __init__(self, user_id, description, type_id, module_id, time):
		self.user_id = user_id
		self.description = description
		self.type_id = type_id
		self.module_id = module_id
		self.time = time

	def __repr__(self):
		return f'({self.type}, {self.module}): {self.date} {self.time} - {self.description}'