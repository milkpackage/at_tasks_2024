# General task
# 1. Make up one simple UI end-to-end test case for your test page from Task_10
# 2. Automate that scenario using WebDriver
# 3. Create PageObject (use Business object if need)for all pages used in scenario



import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from home_page import HomePage
import time

# pytest test_flow.py -v

class TestFlow:
    @pytest.fixture
    def driver(self):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.maximize_window()
        yield driver
        driver.quit()

    def test_about_us_video_flow(self, driver):
        home_page = HomePage(driver)

        home_page.open_page()
        time.sleep(2)

        about_us_page = home_page.click_about_us()
        time.sleep(1)

        assert about_us_page.is_video_modal_open(), "About Us modal is not visible"

        about_us_page.play_video()
        time.sleep(2)

        about_us_page.close_video()
        time.sleep(1)