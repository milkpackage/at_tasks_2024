from selenium.webdriver.common.by import By
from core.web_element_wrapper import Element
from page_objects.base_page import BasePage

class ProjectPage(BasePage):
   def __init__(self, driver):
       super().__init__(driver)
       self.url = "http://localhost/manage_proj_create_page.php"
       self.name_input = Element(driver, By.NAME, "name")
       self.description_textarea = Element(driver, By.NAME, "description")
       self.status_select = Element(driver, By.NAME, "status")
       self.view_status_select = Element(driver, By.NAME, "view_state")
       self.add_button = Element(driver, By.CSS_SELECTOR, "input[type='submit']")

   def create_project(self, name, description="", status="development", view_status="public"):
       self.driver.get(self.url)
       self.name_input.send_keys(name)
       self.description_textarea.send_keys(description)
       self.status_select.select_by_visible_text(status)
       self.view_status_select.select_by_visible_text(view_status)
       self.add_button.click()
       return "project" in self.driver.page_source