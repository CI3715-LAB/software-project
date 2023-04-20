import unittest
from flask import url_for
from SeleniumBaseTestCase import SeleniumBaseTestCase
from selenium.webdriver.common.by import By

from helpers.login_user_front import TITLE, login_user

class TestNavigation(SeleniumBaseTestCase):
	@login_user
	def test_nav_user_list(self):
		self.driver.get(self.get_server_url())
		user_list = self.driver.find_element(By.ID, "user-link")
		user_list.click()

		# assert that we are in the user list page
		self.assertIn(url_for('user.retrieve_users'), self.driver.current_url)
		self.assertIn("<h1>Usuarios</h1>", self.driver.page_source)
	
	@login_user
	def test_nav_user_register(self):
		self.driver.get(self.get_server_url())
		user_register = self.driver.find_element(By.ID, "userRegister-link")
		user_register.click()

		# assert that we are in the user register page
		self.assertIn(url_for('user.user_register'), self.driver.current_url)
		self.assertIn("<h1>Registro de usuario</h1>", self.driver.page_source)

	@login_user
	def test_nav_user_register_from_list(self):
		self.driver.get(self.get_server_url() + url_for('user.retrieve_users'))
		user_register = self.driver.find_element(By.ID, "register")
		user_register.click()

		# assert that we are in the user register page
		self.assertIn(url_for('user.user_register'), self.driver.current_url)
		self.assertIn("<h1>Registro de usuario</h1>", self.driver.page_source)

	@login_user
	def test_nav_user_reset(self):
		self.driver.get(self.get_server_url())
		user_reset = self.driver.find_element(By.ID, "userReset-link")
		user_reset.click()

		# assert that we are in the user reset page
		self.assertIn(url_for('user.user_reset'), self.driver.current_url)
		self.assertIn("<h1>Reinicio de Contraseña</h1>", self.driver.page_source)

	@login_user
	def test_nav_project_list(self):
		self.driver.get(self.get_server_url())
		project_list = self.driver.find_element(By.ID, "project-link")
		project_list.click()

		# assert that we are in the project list page
		self.assertIn(url_for('project.retrieve_projects'), self.driver.current_url)
		self.assertIn("<h1>Proyectos</h1>", self.driver.page_source)

	@login_user
	def test_nav_add_project_from_list(self):
		self.driver.get(self.get_server_url())
		project_list = self.driver.find_element(By.ID, "project-link")
		project_list.click()
		project_add = self.driver.find_element(By.ID, "add")
		project_add.click()

		# assert that we are in the project add page
		self.assertIn(url_for('project.add_project'), self.driver.current_url)
		self.assertIn("<h1>Agregar un nuevo proyecto</h1>", self.driver.page_source)

	@login_user
	def test_nav_client(self):
		self.driver.get(self.get_server_url())
		client = self.driver.find_element(By.ID, "client-link")
		client.click()

		# assert that we are in the client page
		self.assertIn(url_for('client.retrieve_clients'), self.driver.current_url)
		self.assertIn("<h1>Clientes</h1>", self.driver.page_source)
	
	@login_user
	def test_nav_vehicle(self):
		self.driver.get(self.get_server_url())
		vehicle = self.driver.find_element(By.ID, "vehicle-link")
		vehicle.click()

		# assert that we are in the vehicle page
		self.assertIn(url_for('vehicle.retrieve_vehicles'), self.driver.current_url)
		self.assertIn("<h1>Vehiculos</h1>", self.driver.page_source)

	@login_user
	def test_nav_log(self):
		self.driver.get(self.get_server_url())
		log = self.driver.find_element(By.ID, "log-link")
		log.click()

		# assert that we are in the log page
		self.assertIn(url_for('log.retrieve_logs'), self.driver.current_url)
		self.assertIn("<h1>Logger de Eventos</h1>", self.driver.page_source)

	def test_nav_login(self):
		self.driver.get(self.get_server_url())
		login = self.driver.find_element(By.ID, "login-link")
		login.click()

		# assert that we are in the login page
		self.assertIn(url_for('user.user_login'), self.driver.current_url)
		self.assertIn("<h1>Inicio de sesión</h1>", self.driver.page_source)

if __name__ == "__main__":
	unittest.main()