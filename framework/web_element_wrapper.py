from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Element:
    def __init__(self, web_element: WebElement):
        self._element = web_element

    def click(self):
        WebDriverWait(self._element.parent, 10).until(
            EC.element_to_be_clickable(self._element)
        )
        self._element.click()

    def send_keys(self, value):
        WebDriverWait(self._element.parent, 10).until(
            EC.visibility_of(self._element)
        )
        self._element.send_keys(value)

    @property
    def text(self):
        return self._element.text