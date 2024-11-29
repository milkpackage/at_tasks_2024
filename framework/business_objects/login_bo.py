from page_objects.login_page import LoginPage
import logging

logger = logging.getLogger(__name__)

class LoginBO:
    def __init__(self, driver):
        self.login_page = LoginPage(driver)
        self.driver = driver

    def login(self, username: str, password: str) -> bool:
        try:
            self.login_page.login(username, password)
            return "administrator" in self.driver.page_source or "AQA Testing" in self.driver.page_source
        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
            return False