from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
 
from config.setup import db

# Permission model
class Permission (db.Model):
    __tablename__ = "app_permission"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('app_module.id'), nullable=False)

    def __init__(self, name, type, module_id):
        self.name = name
        self.type = type
        self.module_id = module_id

    def __repr__(self):
        return f'{self.type}, {self.module.name}'


# Intermediate table role_permission
app_role_permission = db.Table('app_role_permission',
        db.Column('role_id', db.Integer, db.ForeignKey('app_role.id')),
        db.Column('permission_id', db.Integer, db.ForeignKey('app_permission.id'))
    )


# Role model
class Role (db.Model):
    __tablename__ = "app_role"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    
    # one to many relationship with user
    users = db.relationship('User', backref='role', lazy=True)
    # many to many relationship with permission
    permissions = db.relationship('Permission', secondary=app_role_permission, backref='roles')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'{self.name}'


# User model
class User (db.Model):
    __tablename__ = "app_user"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    date_joined = db.Column(db.Date, default=datetime.utcnow)
   
    # foreign key to role
    role_id = db.Column(db.Integer, db.ForeignKey('app_role.id'), nullable=False)
    # foreign key to project
    project_id = db.Column(db.Integer, db.ForeignKey('app_project.id', use_alter=True), nullable=True, default=0)
    # foreign key to department
    department_id = db.Column(db.Integer, db.ForeignKey('app_department.id'), nullable=False, default=0)

    project = db.relationship('Project', backref='user', lazy=True, foreign_keys=[project_id])

    def generate_password(self, password):
        return generate_password_hash(password)
     
    def check_password(self, password):
        return check_password_hash(self.password,password)

    def __init__(self, username, password, name, lastname, role_id, project_id=0, department_id=0):
        self.username = username
        self.password = self.generate_password(password)
        self.name = name
        self.lastname = lastname
        self.role_id = role_id
        self.project_id = project_id
        self.department_id = department_id

    def __repr__(self):
        return f'{self.username}'

