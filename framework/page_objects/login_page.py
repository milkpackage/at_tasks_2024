from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from core.web_element_wrapper import Element
from page_objects.base_page import BasePage
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost/" 
        self.username_input = Element(driver, By.CSS_SELECTOR, "input#username")
        self.login_button = Element(driver, By.CSS_SELECTOR, "input[type='submit'], button.width-40.pull-right.btn.btn-success.btn-inverse.bigger-110")
        self.password_input = Element(driver, By.CSS_SELECTOR, "input[type='password']")

    def open(self):
        logger.debug(f"Opening URL: {self.url}")
        self.driver.get(self.url)
        logger.debug(f"Current URL: {self.driver.current_url}")
        return self

    #added logger to see where i got error 
    def login(self, username, password):
        try:
            logger.debug("Starting login process")
            self.open()
            
            self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input#username")))
            
            logger.debug(f"Entering username: {username}")
            self.username_input.send_keys(username)
            
            logger.debug("Clicking login button")
            self.login_button.click()
            
            logger.debug("Waiting for password field")
            self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
            
            logger.debug("Entering password")
            self.password_input.send_keys(password)
            
            logger.debug("Clicking final submit")
            self.login_button.click()
            
            return self
            
        except Exception as e:
            logger.error(f"Login failed with error: {str(e)}")
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"error_screenshot_{timestamp}.png"
            self.driver.save_screenshot(screenshot_path)
            logger.error(f"Screenshot saved to {screenshot_path}")
            raise