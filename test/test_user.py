import unittest
import requests

from user.model import User
from app import db

class UserTest(unittest.TestCase):
    BASE_URL = 'http://localhost:5000'
    USER_URL = '{}/user'.format(BASE_URL)
    USER_ADMIN = {
        'username': 'admin',
        'password': 'admin',
    }
    USER_EXAMPLE = {
        'username': 'example',
        'email': 'example@example.com',
        'password': 'example',
        'admin': 'on'
    }
    BAD_USER_REGISTER = {
        'username': '',
        'email': 'example@example.com',
        'password': 'example',
        'admin': 'on'
    }
    BAD_USER_LOGIN = {
        'username': '',
        'password': 'example'
    }

    # log in
    def test_login(self):
        r = requests.post(self.USER_URL + '/login', data=self.USER_ADMIN)

        # load page without errors
        self.assertEqual(r.status_code, 200)

    # user list only shown to admins
    def test_user_list(self):
        r = requests.get(self.USER_URL)

        # load page without errors
        self.assertEqual(r.status_code, 200)
        
    # register a new user by an admin
    def test_register(self):
        # restart db
        User.query.filter_by(username="example").delete()
        db.session.commit()

        # register user example
        r = requests.post(self.USER_URL + '/register', data=self.USER_EXAMPLE)

        # load page without errors
        self.assertEqual(r.status_code, 200)

        # restart db
        User.query.filter_by(username="example").delete()
        db.session.commit()

    # logout
    def test_logout(self):
        # user in session
        # self.assertIsNotNone(session['user'])

        # logout user
        r = requests.get(self.USER_URL + '/logout')

        # user logged out
        # self.assertNotIn('user', session)

        # load page without errors
        self.assertEqual(r.status_code, 200)

    # INCORRECT LOGIN AND REGISTER
    # def test_incorrect_login(self):
    #     # login bad user
    #     r = requests.post(self.USER_URL + '/login', data=self.BAD_USER_LOGIN)
    #     # test redirect to error
    #     self.assertEqual(r.url, self.BASE_URL+'/error')
    #     # load page without errors
    #     self.assertEqual(r.status_code, 200)

    # def test_incorrect_register(self):
    #     # register bad user
    #     r = requests.post(self.USER_URL + '/register', data=self.BAD_USER_REGISTER)
    #     # test redirect to error
    #     self.assertEqual(r.url, self.BASE_URL+'/error')
    #     # load page without errors
    #     self.assertEqual(r.status_code, 200)