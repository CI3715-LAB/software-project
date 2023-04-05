import functools

from flask import url_for
from selenium.webdriver.common.by import By

from .init_database import USER_LOGIN_DATA

TITLE = "Flask App"


def login_user(fun):
	@functools.wraps(fun)
	def wrapper(*args, **kwargs):
		self = args[0]
		self.driver.get(self.get_server_url() + url_for('user.user_login'))
		username = self.driver.find_element(By.NAME, "username")
		password = self.driver.find_element(By.NAME, "password")
		username.send_keys(USER_LOGIN_DATA["username"])
		password.send_keys(USER_LOGIN_DATA["password"])
		submit = self.driver.find_element(By.ID, "submit")
		submit.click()
		return fun(*args, **kwargs)
	return wrapper