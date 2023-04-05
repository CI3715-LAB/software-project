import unittest
from BaseTestCase import BaseTestCase, db

from helpers.login_user_back import login_user

class TestVehicle(BaseTestCase):
	@login_user
	def test_vehicle_list(self):
		response = self.client.get('/vehicle/')
		self.assert200(response)

if __name__ == "__main__":
	unittest.main()