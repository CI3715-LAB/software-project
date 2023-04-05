import unittest

from flask import url_for
from selenium.webdriver.common.by import By
from SeleniumBaseTestCase import SeleniumBaseTestCase
from helpers.login_user_front import login_user

class TestFrontEndLog(SeleniumBaseTestCase):
	@login_user
	def test_log_list_display(self):
		self.driver.get(self.get_server_url() + url_for('log.retrieve_logs'))
		self.assertIn("<h1>Logger de Eventos</h1>", self.driver.page_source)

if __name__ == "__main__":
	unittest.main()