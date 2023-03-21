import sys
sys.path.append("../")
from flask_testing import TestCase
from app import db, create_app
from project.model import Project
from user.model import User, Role
from werkzeug.security import generate_password_hash
from datetime import datetime

class BaseTestCase(TestCase):
	def create_app(self):
		return create_app('config.setup.TestConfig')

	def setUp(self):
		# db.drop_all()
		db.create_all()
		project_undefined = Project('Undefined', datetime.fromisoformat('2023-01-01'), datetime.fromisoformat('2023-01-01'), True)
		project_undefined.id = 0;
		db.session.add(project_undefined)
		db.session.add(Project('Test Project', datetime.fromisoformat('2023-01-01'), datetime.fromisoformat('2023-01-01'), True))
		db.session.add(Role('admin'))
		db.session.add(User('testUser', 'test', 'testName', 'testLastName', 1, 1))
		db.session.commit()

	def tearDown(self):
		db.session.remove()
		db.session.close()
		db.drop_all()