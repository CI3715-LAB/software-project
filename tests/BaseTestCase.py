import sys
sys.path.append("../")
from flask_testing import TestCase
from app import db, create_app
from helpers.init_database import init_database

class BaseTestCase(TestCase):
	def create_app(self):
		return create_app('config.setup.TestConfig')

	def setUp(self):
		db.drop_all()
		db.create_all()
		init_database(self, db)

	def tearDown(self):
		db.session.remove()
		db.session.close()
		db.drop_all()