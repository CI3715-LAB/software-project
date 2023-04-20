import sys
sys.path.append("../software-project_master")
from app import db, create_app
from sqlalchemy import text

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
		self.driver.close()
		self.driver.quit()