import unittest

from flask import url_for
from selenium.webdriver.common.by import By
from SeleniumBaseTestCase import SeleniumBaseTestCase, db
from project.model import Project
from helpers.login_user_front import login_user
from datetime import date

class TestFrontEndClient(SeleniumBaseTestCase):
	@login_user
	def test_client_list_display(self):
		self.driver.get(self.get_server_url() + url_for('client.retrieve_clients'))
		self.assertIn("<h1>Clientes</h1>", self.driver.page_source)

if __name__ == "__main__":
	unittest.main()