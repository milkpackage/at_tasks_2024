from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ElementWrapper:
    def __init__(self, driver, locator):
        self.driver = driver
        self.locator = locator
        self.wait = WebDriverWait(driver, 10)

    def find(self):
        logger.info(f"Finding element: {self.locator}")
        return self.wait.until(EC.presence_of_element_located(self.locator))

    def click(self):
        logger.info(f"Clicking element: {self.locator}")
        element = self.wait.until(EC.element_to_be_clickable(self.locator))
        element.click()
        return self

    def type(self, text):
        logger.info(f"Typing text: {text}")
        element = self.find()
        element.clear()
        element.send_keys(text)
        return self


class DropdownWrapper(ElementWrapper):
    def select_by_text(self, text):
        logger.info(f"Selecting option: {text}")
        self.click()
        time.sleep(1)

        #trying selectors
        selectors = [
            f"//div[contains(text(), '{text}')]",
            f"//span[contains(text(), '{text}')]",
            f"//button[contains(text(), '{text}')]",
            f"//*[@data-value='{text}']"
        ]

        for xpath in selectors:
            try:
                option = (By.XPATH, xpath)
                ElementWrapper(self.driver, option).click()
                return self
            except:
                continue

        logger.error(f"Could not find option: {text}")
        return self

    def select_by_index(self, index):
        logger.info(f"Selecting option by index: {index}")
        self.click()
        time.sleep(1)

        selectors = [
            f"div:nth-child({index + 1})",
            f"button:nth-child({index + 1})",
            f"li:nth-child({index + 1})"
        ]

        for css in selectors:
            try:
                option = (By.CSS_SELECTOR, css)
                ElementWrapper(self.driver, option).click()
                return self
            except:
                continue

        logger.error(f"Could not find option at index: {index}")
        return self


class PageFactory:
    def __init__(self, driver):
        self.driver = driver

    def get_element(self, locator):
        return ElementWrapper(self.driver, locator)

    def get_dropdown(self, locator):
        return DropdownWrapper(self.driver, locator)