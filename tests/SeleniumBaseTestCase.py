import sys
sys.path.append("../proyecto")
from app import db, create_app
from helpers.init_database import init_database

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
		db.drop_all()
		db.create_all()
		init_database(self, db)

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