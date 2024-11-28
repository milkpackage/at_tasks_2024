from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import logging

logger = logging.getLogger(__name__)

class Element:
    def __init__(self, driver, by, value):
        self.driver = driver
        self.locator = (by, value)
        self.wait = WebDriverWait(driver, 10)
        
    def find(self):
        logger.debug(f"Finding element with locator: {self.locator}")
        return self.wait.until(EC.presence_of_element_located(self.locator))
        
    def send_keys(self, value):
        logger.debug(f"Sending keys '{value}' to element with locator: {self.locator}")
        self.find().send_keys(value)
        
    def click(self):
        logger.debug(f"Clicking element with locator: {self.locator}")
        self.wait.until(EC.element_to_be_clickable(self.locator)).click()

    def select_by_visible_text(self, text):
        select = Select(self.find())
        select.select_by_visible_text(text)

    def select_by_value(self, value):
        select = Select(self.find())
        select.select_by_value(value)


    def text(self):
        return self.find().text
        
    def is_displayed(self):
        try:
            return self.find().is_displayed()
        except:
            return False