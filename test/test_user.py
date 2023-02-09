import unittest
import requests

from user.model import User

class UserTest(unittest.TestCase):
    BASE_URL = 'http://localhost:5000'
    USER_URL = '{}/user'.format(BASE_URL)
    USER_ADMIN_OBJ = [
        'username' = 'example',
        'email' = 'example@example.com',
        'password' = 'example',
        'admin' = 'on'
    ]

    def test_should_retrieve_all_users(self):
        r = requests.get(self.USER_URL)
        self.assertEqual(r.status_code, 200)

    """ def test_should_register_a_new_user(self):
        r = requests.post(self.USER_URL + '/register', data=self.USER_ADMIN_OBJ)
        self.assertEqual(r.status_code, 200) """