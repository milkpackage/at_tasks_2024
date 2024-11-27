from selenium.webdriver.support.wait import WebDriverWait
from core.page_factory import PageFactory

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        PageFactory.init_elements(self)