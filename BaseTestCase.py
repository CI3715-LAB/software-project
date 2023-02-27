from flask_testing import TestCase
from app import db
from project.model import Project
from user.model import User, Role
from werkzeug.security import generate_password_hash
from datetime import datetime

from flask_assets import Environment, Bundle
from flask import Flask


class BaseTestCase(TestCase):
	def create_app(self):
		app = Flask(__name__)
		app.config.from_object('config.setup.TestConfig')

		# Assets Bundle initialization
		assets = Environment(app)
		assets.url = app.static_url_path
		scss = Bundle('scss/*.scss', filters='pyscss, cssmin', output='css/all.css')
		assets.register('scss_all', scss)

		# db = SQLAlchemy(app)
		db.init_app(app)

		from user.endpoint import user_blueprint
		from project.endpoint import project_blueprint
		from log.endpoint import log_blueprint

		app.register_blueprint(user_blueprint, url_prefix='/user')
		app.register_blueprint(project_blueprint, url_prefix='/project')
		app.register_blueprint(log_blueprint, url_prefix='/log')
		return app

	def setUp(self):
		# db.drop_all()
		db.create_all()
		project_undefined = Project('Undefined', datetime.fromisoformat('2023-01-01'), datetime.fromisoformat('2023-01-01'), True)
		project_undefined.id = 0;
		db.session.add(project_undefined)
		db.session.add(Project('Test Project', datetime.fromisoformat('2023-01-01'), datetime.fromisoformat('2023-01-01'), True))
		db.session.add(Role('admin'))
		db.session.add(User('testUser', generate_password_hash('test'), 'testName', 'testLastName', 1, 1))
		db.session.commit()

	def tearDown(self):
		db.session.remove()
		db.session.close()
		db.drop_all()