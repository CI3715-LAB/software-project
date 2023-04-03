import sys
sys.path.append("../")
from flask_testing import TestCase
from app import db, create_app
from project.model import Project
from user.model import User, Role
from department.model import Department
from log.model import Log, Type, Module
from werkzeug.security import generate_password_hash
from datetime import datetime

class BaseTestCase(TestCase):
	def create_app(self):
		return create_app('config.setup.TestConfig')

	def setUp(self):
		db.create_all()
		project_undefined = Project('Undefined', datetime.fromisoformat('2023-01-01'), datetime.fromisoformat('2023-01-01'), True)
		project_undefined.id = 0
		db.session.add(project_undefined)
		db.session.add(Project('Test Project', datetime.fromisoformat('2023-01-01'), datetime.fromisoformat('2023-01-01'), True))
		db.session.add(Role('admin'))
		department_undefined = Department('Undefined')
		department_undefined.id = 0
		db.session.add(department_undefined)
		db.session.add(Department('Test Department'))
		db.session.add(User('testUser', 'test', 'testName', 'testLastName', 1, 1, 1))
		db.session.add(User('testUser2', 'test', 'testName2', 'testLastName2', 1, 1, 1))
		db.session.add(Module('Usuarios'))
		db.session.add(Module('Proyectos'))
		db.session.add(Module('Vehiculos'))
		db.session.add(Module('Clientes'))
		db.session.add(Module('Departamentos'))
		db.session.add(Type('Agregar'))
		db.session.add(Type('Buscar'))
		db.session.add(Type('Modificar'))
		db.session.add(Type('Eliminar'))
		db.session.commit()

	def tearDown(self):
		db.session.remove()
		db.session.close()
		db.drop_all()