import sys
sys.path.append("../")
import urllib.request as urllib2
from app import db, create_app
from project.model import Project
from user.model import User, Role
from log.model import Log, Type, Module
from datetime import datetime

# Modules needed for selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller


from flask_testing import LiveServerTestCase
class SeleniumBaseTestCase(LiveServerTestCase):
	def create_app(self):
		self.app = create_app('config.setup.SeleniumTestConfig')
		return self.app

	def setUp(self):
		# Database
		db.session.commit()
		db.drop_all()
		db.create_all()
		project_undefined = Project('Undefined', datetime.fromisoformat('2023-01-01'), datetime.fromisoformat('2023-01-01'), True)
		project_undefined.id = 0;
		db.session.add(project_undefined)
		db.session.add(Project('Test Project', datetime.fromisoformat('2023-01-01'), datetime.fromisoformat('2023-01-01'), True))
		db.session.add(Role('admin'))
		db.session.add(User('testUser', 'test', 'testName', 'testLastName', 1, 1))
		db.session.add(User('testUser2', 'test', 'testName2', 'testLastName2', 1, 1))
		db.session.add(Type('Usuarios'))
		db.session.add(Type('Proyectos'))
		db.session.add(Type('Vehiculos'))
		db.session.add(Type('Clientes'))
		db.session.add(Module('Agregar'))
		db.session.add(Module('Buscar'))
		db.session.add(Module('Modificar'))
		db.session.add(Module('Eliminar'))
		db.session.commit()

		# Selenium
		chromedriver_autoinstaller.install()
		chrome_options = Options()
		chrome_options.add_argument("--headless") # Ensure GUI is off
		chrome_options.add_argument("--no-sandbox")
		self.driver = webdriver.Chrome(options=chrome_options)

	def tearDown(self):
		db.session.remove()
		db.session.close()
		db.drop_all()
		self.driver.quit()