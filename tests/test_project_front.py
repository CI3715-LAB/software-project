import unittest

from flask import url_for
from selenium.webdriver.common.by import By
from SeleniumBaseTestCase import SeleniumBaseTestCase, db
from project.model import Project
from helpers.login_user_front import login_user
from datetime import date

class TestFrontEndProject(SeleniumBaseTestCase):
	@login_user
	def test_project_list_display(self):
		self.driver.get(self.get_server_url() + url_for('project.retrieve_projects'))
		self.assertIn("<h1>Proyectos</h1>", self.driver.page_source)

		for project in db.session.query(Project).all():
			if project.id == 0: continue
			form = self.driver.find_element(By.ID, f"form-edit-{project.id}")
			id = form.find_element(By.NAME, "id").get_attribute("value")
			description = form.find_element(By.NAME, "description").get_attribute("value")
			open_date = form.find_element(By.NAME, "open_date").get_attribute("value")
			close_date = form.find_element(By.NAME, "close_date").get_attribute("value")
			open_date = date.fromisoformat(open_date)
			close_date = date.fromisoformat(close_date)
			self.assertEqual(project.id, int(id))
			self.assertEqual(project.description, description)
			self.assertEqual(project.open_date, open_date)
			self.assertEqual(project.close_date, close_date)

	@login_user
	def test_project_add(self):
		self.driver.get(self.get_server_url() + url_for('project.add_project'))
		description = self.driver.find_element(By.NAME, "description")
		open_date = self.driver.find_element(By.NAME, "open_date")
		close_date = self.driver.find_element(By.NAME, "close_date")
		submit = self.driver.find_element(By.ID, "submit")

		# add a new project
		description.send_keys("Test project2")
		# locale is set as en_US, so the date format is mm/dd/yyyy
		open_date.send_keys("10/23/2020")
		close_date.send_keys("12/22/2020")
		submit.click()

		# assert that we are in the project list page
		self.assertIn(url_for('project.retrieve_projects'), self.driver.current_url)
		self.assertIn("<h1>Proyectos</h1>", self.driver.page_source)
		self.assertIn("Test project2", self.driver.page_source)

		# assert that the project was added to the database
		project = db.session.query(Project).filter_by(description="Test project2").first()
		self.assertIsNotNone(project)
		self.assertEqual(project.description, "Test project2")
		self.assertEqual(project.open_date, date.fromisoformat("2020-10-23"))
		self.assertEqual(project.close_date, date.fromisoformat("2020-12-22"))

	@login_user
	def test_project_edit(self):
		self.driver.get(self.get_server_url() + url_for('project.retrieve_projects'))
		self.driver.find_element(By.ID, "form-edit-1").submit()
		description = self.driver.find_element(By.NAME, "description")
		open_date = self.driver.find_element(By.NAME, "open_date")
		close_date = self.driver.find_element(By.NAME, "close_date")
		edit = self.driver.find_element(By.ID, "edit-for-1")

		# edit the project
		description.clear()
		description.send_keys("Test project edited")
		open_date.clear()
		open_date.send_keys("10/23/2023")
		close_date.clear()
		close_date.send_keys("12/22/2023")
		edit.click()

		# assert that we are in the project list page and project was edited
		self.assertIn(url_for('project.retrieve_projects'), self.driver.current_url)
		self.driver.refresh()
		self.assertIn("Test project edited", self.driver.page_source)

		# assert that the project was edited in the database
		project = db.session.query(Project).filter_by(id=1).first()
		self.assertIsNotNone(project)
		self.assertEqual(project.description, "Test project edited")
		self.assertEqual(project.open_date, date.fromisoformat("2023-10-23"))
		self.assertEqual(project.close_date, date.fromisoformat("2023-12-22"))

	@login_user
	def test_project_delete(self):
		self.driver.get(self.get_server_url() + url_for('project.retrieve_projects'))
		project = db.session.query(Project).filter_by(id=4).first()
		self.assertIn(project.description, self.driver.page_source)
		self.driver.find_element(By.ID, "delete-for-4").click()

		# assert that we are in the project list page and project was deleted
		self.assertIn(url_for('project.retrieve_projects'), self.driver.current_url)
		self.driver.refresh()
		self.assertNotIn(project.description, self.driver.page_source)

		# assert that the project was deleted from the database
		project = db.session.query(Project).filter_by(id=4).first()
		self.assertIsNone(project)

	@login_user
	def test_project_toggle_off(self):
		self.driver.get(self.get_server_url() + url_for('project.retrieve_projects'))
		project = db.session.query(Project).filter_by(id=1).first()
		self.assertTrue(project.enabled)
		self.driver.find_element(By.ID, "toggle-for-1").click()
		db.session.commit()

		# assert that we are in the project list page and project was toggled off
		self.assertIn(url_for('project.retrieve_projects'), self.driver.current_url)
		form = self.driver.find_element(By.ID, "form-edit-1")
		inputs = form.find_elements(By.CLASS_NAME, "disabled")
		self.assertEqual(len(inputs), 4)

		# assert that the project was toggled off in the database
		project = db.session.query(Project).filter_by(id=1).first()
		self.assertIsNotNone(project)
		self.assertFalse(project.enabled)

	@login_user
	def test_project_toggle_on(self):
		# set the project as disabled
		project = db.session.query(Project).filter_by(id=1).first()
		project.enabled = False
		db.session.commit()

		# toggle on the project
		self.driver.get(self.get_server_url() + url_for('project.retrieve_projects'))
		self.driver.find_element(By.ID, "toggle-for-1").click()
		db.session.commit()

		# assert that we are in the project list page and project was toggled on
		self.assertIn(url_for('project.retrieve_projects'), self.driver.current_url)
		form = self.driver.find_element(By.ID, "form-edit-1")
		inputs = form.find_elements(By.CLASS_NAME, "disabled")
		self.assertEqual(len(inputs), 0)

		# assert that the project was toggled on in the database
		project = db.session.query(Project).filter_by(id=1).first()
		self.assertIsNotNone(project)
		self.assertTrue(project.enabled)

if __name__ == "__main__":
	unittest.main()