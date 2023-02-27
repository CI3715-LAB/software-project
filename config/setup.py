# Load env variables
from os import environ

SECRET_KEY=environ.get('SECRET_KEY')

# SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class DevelopmentConfig(object):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///sqlite.db'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	TEMPLATES_AUTO_RELOAD = True
	SECRET_KEY = SECRET_KEY
	
class TestConfig(object):
	DEBUG = True
	TESTING = True
	WTF_CSRF_ENABLED = False
	SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
	SECRET_KEY = 'test'

# Logger
from log.utils import Logger

logger = Logger()