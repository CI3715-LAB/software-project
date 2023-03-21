import unittest

from flask import url_for
from selenium.webdriver.common.by import By
from SeleniumBaseTestCase import SeleniumBaseTestCase, User, db
from helpers.login_user_front import (
	DELETE_USER, INVALID_USER,
    INVALID_USER_PASSWORD, REGISTER_USER,
	VALID_USER, login_user
)

class TestFrontEndUser(SeleniumBaseTestCase):
	def test_user_login(self):
		self.driver.get(self.get_server_url() + url_for('user.user_login'))
		username = self.driver.find_element(By.NAME, "username")
		password = self.driver.find_element(By.NAME, "password")
		submit = self.driver.find_element(By.ID, "submit")

		# login with valid user
		username.send_keys(VALID_USER["username"])
		password.send_keys(VALID_USER["password"])
		submit.click()

		# assert that we are in the home page and the user is logged in
		self.assertIn(f"Bienvenido {VALID_USER['username']}", self.driver.page_source)
		self.assertIn(url_for('home'), self.driver.current_url)
	
	def test_user_login_invalid_username(self):
		self.driver.get(self.get_server_url() + url_for('user.user_login'))
		username = self.driver.find_element(By.NAME, "username")
		password = self.driver.find_element(By.NAME, "password")
		submit = self.driver.find_element(By.ID, "submit")

		# login with invalid user and assert error message
		username.send_keys(INVALID_USER["username"])
		password.send_keys(INVALID_USER["password"])
		submit.click()
		self.assertIn(url_for('user.user_login'), self.driver.current_url)
		self.assertIn("<h4>El nombre de usuario suministrado no existe</h4>", self.driver.page_source)

	def test_user_login_invalid_password(self):
		self.driver.get(self.get_server_url() + url_for('user.user_login'))
		username = self.driver.find_element(By.NAME, "username")
		password = self.driver.find_element(By.NAME, "password")
		submit = self.driver.find_element(By.ID, "submit")

		# login with invalid user and assert error message
		username.send_keys(INVALID_USER_PASSWORD["username"])
		password.send_keys(INVALID_USER_PASSWORD["password"])
		submit.click()
		self.assertIn(url_for('user.user_login'), self.driver.current_url)
		self.assertIn("<h4>Las credenciales suministradas no son validas</h4>", self.driver.page_source)

	@login_user
	def test_user_list_display(self):
		self.driver.get(self.get_server_url() + url_for('user.retrieve_users'))

		# assert that the user list is the same as the database
		for user in db.session.query(User).all():
			form = self.driver.find_element(By.ID, f"form-edit-{user.id}")
			id = form.find_element(By.NAME, "id").get_attribute("value")
			username = form.find_element(By.NAME, "username").get_attribute("value")
			name = form.find_element(By.NAME, "name").get_attribute("value")
			lastname = form.find_element(By.NAME, "lastname").get_attribute("value")
			role = form.find_element(By.NAME, "role").get_attribute("value")
			project = form.find_element(By.NAME, "project").get_attribute("value")
			self.assertEqual(id, str(user.id))
			self.assertEqual(username, user.username)
			self.assertEqual(name, user.name)
			self.assertEqual(lastname, user.lastname)
			self.assertEqual(role, str(user.role))
			self.assertEqual(project, str(user.project))

	@login_user
	def test_user_register(self):
		self.driver.get(self.get_server_url() + url_for('user.user_register'))
		username = self.driver.find_element(By.NAME, "username")
		password = self.driver.find_element(By.NAME, "password")
		name = self.driver.find_element(By.NAME, "name")
		lastname = self.driver.find_element(By.NAME, "lastname")
		role = self.driver.find_element(By.NAME, "role")
		project = self.driver.find_element(By.NAME, "project")
		submit = self.driver.find_element(By.ID, "submit")

		# register a new user
		username.send_keys(REGISTER_USER["username"])
		password.send_keys(REGISTER_USER["password"])
		name.send_keys(REGISTER_USER["name"])
		lastname.send_keys(REGISTER_USER["lastname"])
		role.click()
		role.find_element(By.XPATH, f"//option[@value = \"{REGISTER_USER['project']}\"]").click()
		project.click()
		project.find_element(By.XPATH, f"//option[@value = \"{REGISTER_USER['project']}\"]").click()
		submit.click()

		# assert that the user is registered
		self.assertIn(url_for('user.retrieve_users'), self.driver.current_url)
		user = db.session.query(User).filter_by(username=REGISTER_USER["username"]).first()
		form = self.driver.find_element(By.ID, f"form-edit-{user.id}")
		id = form.find_element(By.NAME, "id").get_attribute("value")
		username = form.find_element(By.NAME, "username").get_attribute("value")
		name = form.find_element(By.NAME, "name").get_attribute("value")
		lastname = form.find_element(By.NAME, "lastname").get_attribute("value")
		role = form.find_element(By.NAME, "role").get_attribute("value")
		project = form.find_element(By.NAME, "project").get_attribute("value")
		self.assertEqual(id, str(user.id))
		self.assertEqual(username, user.username)
		self.assertEqual(name, user.name)
		self.assertEqual(lastname, user.lastname)
		self.assertEqual(role, str(user.role))
		self.assertEqual(project, str(user.project))

	@login_user
	def test_user_reset(self):
		self.driver.get(self.get_server_url() + url_for('user.user_reset'))
		username = self.driver.find_element(By.NAME, "username")
		password = self.driver.find_element(By.NAME, "password_prev")
		password_new = self.driver.find_element(By.NAME, "password_next")
		submit = self.driver.find_element(By.ID, "submit")

		# reset the user password
		username.send_keys(VALID_USER["username"])
		password.send_keys(VALID_USER["password"])
		password_new.send_keys("new_password")
		submit.click()

		# assert that the user password is reset
		self.driver.find_element(By.ID, "logout-link").click()
		self.driver.get(self.get_server_url() + url_for('user.user_login'))
		username = self.driver.find_element(By.NAME, "username")
		password = self.driver.find_element(By.NAME, "password")
		submit = self.driver.find_element(By.ID, "submit")
		username.send_keys(VALID_USER["username"])
		password.send_keys("new_password")
		submit.click()
		self.assertIn(url_for('home'), self.driver.current_url)
		self.assertIn(f"<h1>Bienvenido {VALID_USER['username']}</h1>", self.driver.page_source)

	@login_user
	def test_user_edit(self):
		self.driver.get(self.get_server_url() + url_for('user.retrieve_users'))
		form = self.driver.find_element(By.ID, f"form-edit-{VALID_USER['id']}")
		name = form.find_element(By.NAME, "name")
		lastname = form.find_element(By.NAME, "lastname")
		submit = form.find_element(By.ID, f"edit-for-{VALID_USER['id']}")

		# edit the user
		name.clear()
		name.send_keys("new_name")
		lastname.clear()
		lastname.send_keys("new_lastname")
		submit.click()

		# assert that the user is edited in the database
		user = db.session.query(User).filter_by(username=VALID_USER["username"]).first()
		self.assertEqual(user.name, "new_name")
		self.assertEqual(user.lastname, "new_lastname")

		# assert that the user is edited in the page
		self.assertIn(url_for('user.retrieve_users'), self.driver.current_url)
		self.driver.refresh()
		form = self.driver.find_element(By.ID, f"form-edit-{VALID_USER['id']}")
		id = form.find_element(By.NAME, "id").get_attribute("value")
		username = form.find_element(By.NAME, "username").get_attribute("value")
		name = form.find_element(By.NAME, "name").get_attribute("value")
		lastname = form.find_element(By.NAME, "lastname").get_attribute("value")
		role = form.find_element(By.NAME, "role").get_attribute("value")
		project = form.find_element(By.NAME, "project").get_attribute("value")
		self.assertEqual(id, str(user.id))
		self.assertEqual(username, user.username)
		self.assertEqual(name, "new_name")
		self.assertEqual(lastname, "new_lastname")
		self.assertEqual(role, str(user.role))
		self.assertEqual(project, str(user.project))

	@login_user
	def test_user_delete(self):
		self.driver.get(self.get_server_url() + url_for('user.retrieve_users'))
		submit = self.driver.find_element(By.ID, f"delete-for-{DELETE_USER['id']}")

		# delete the user
		submit.click()

		# assert that the user is deleted in the database
		user = db.session.query(User).filter_by(username=DELETE_USER["username"]).first()
		self.assertIsNone(user)

		# assert that the user is deleted in the page
		self.assertIn(url_for('user.retrieve_users'), self.driver.current_url)
		self.driver.refresh()
		self.assertNotIn(DELETE_USER["username"], self.driver.page_source)



	
if __name__ == "__main__":
	unittest.main()