import sys
sys.path.append("../software-project_master")
from flask_testing import TestCase
from app import db, create_app
from sqlalchemy import text

class BaseTestCase(TestCase):
	def create_app(self):
		return create_app('config.setup.TestConfig')

	def setUp(self):
		with self.app.app_context():
			db.drop_all()
			db.create_all()
		# init_database(self, db)
		# Fill database with initial data
			with open('init.sql') as f:
				for line in f:
					if line.strip() != '' and not line.strip().startswith('--'):
						db.session.execute(text(line.strip()))
				db.session.commit()

	def tearDown(self):
		db.session.remove()
		db.session.close()
		db.drop_all()