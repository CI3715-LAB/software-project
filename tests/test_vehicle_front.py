import unittest

from flask import url_for
from selenium.webdriver.common.by import By
from SeleniumBaseTestCase import SeleniumBaseTestCase, db
from helpers.login_user_front import login_user
from datetime import date

class TestFrontEndVehicle(SeleniumBaseTestCase):
	@login_user
	def test_vehicle_list_display(self):
		self.driver.get(self.get_server_url() + url_for('vehicle.retrieve_vehicles'))
		self.assertIn("<h1>Vehiculos</h1>", self.driver.page_source)

if __name__ == "__main__":
	unittest.main()