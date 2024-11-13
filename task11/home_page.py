from selenium.webdriver.common.by import By
from main_page import MainPage
from about_us_page import AboutUsPage


class HomePage(MainPage):
    ABOUT_US_BUTTON = (By.CSS_SELECTOR, "#navbarExample > ul > li:nth-child(3) > a")

    def open_page(self):
        self.driver.get("https://www.demoblaze.com/")
        return self

    def click_about_us(self):
        self.click_element(self.ABOUT_US_BUTTON)
        return AboutUsPage(self.driver)