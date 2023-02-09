# Load env variables
from os import environ

SECRET_KEY=environ.get('SECRET_KEY')

# SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()