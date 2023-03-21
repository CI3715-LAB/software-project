import functools

from flask import url_for
from selenium.webdriver.common.by import By

VALID_USER = {
	"id": 1,
	"username": "testUser",
	"password": "test"
}

INVALID_USER_PASSWORD = {
	"username": "testUser",
	"password": "invalid_password"
}

INVALID_USER = {
	"username": "invalid_username",
	"password": "test"
}

REGISTER_USER = {
	"username": "testUser3",
	"password": "test",
    "name": "testName3",
    "lastname": "testLastname3",
    "role": "admin",
    "project": "Test Project"
}

DELETE_USER = {
	"id": 2,
	"username": "testUser2",
	"password": "test"
}

TITLE = "Flask App"


def login_user(fun):
	@functools.wraps(fun)
	def wrapper(*args, **kwargs):
		args[0].driver.get(args[0].get_server_url() + url_for('user.user_login'))
		username = args[0].driver.find_element(By.NAME, "username")
		password = args[0].driver.find_element(By.NAME, "password")
		username.send_keys(VALID_USER["username"])
		password.send_keys(VALID_USER["password"])
		submit = args[0].driver.find_element(By.ID, "submit")
		submit.click()
		return fun(*args, **kwargs)
	return wrapper