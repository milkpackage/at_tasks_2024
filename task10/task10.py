#V5 https://www.demoblaze.com/ (About us)

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

about_us_val = "#navbarExample > ul > li:nth-child(3) > a"
url = 'https://www.demoblaze.com/'

class TestAboutUs:
    @pytest.fixture
    def driver(self):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.maximize_window()
        yield driver
        driver.quit()

    #clicking on about us element on a site
    def test_about_us_button(self, driver):
        driver.get(url)
        time.sleep(2)

        about_us = driver.find_element(By.CSS_SELECTOR, about_us_val)

        assert about_us.is_displayed(), "About Us is not visible"
        assert about_us.is_enabled(), "About Us is not clickable"

        about_us.click()
        time.sleep(1)
    #test to check is video player playing video
    def test_video_player(self, driver):
        driver.get(url)
        time.sleep(2)
        about_us = driver.find_element(By.CSS_SELECTOR, about_us_val)
        about_us.click()
        time.sleep(1)

        #find and click video element, after assert that videoplayer is visible
        video_element = driver.find_element(By.CLASS_NAME, "vjs-poster")

        assert video_element.is_displayed(), "Video elements are not visible"

        video_element.click()
        time.sleep(2)
    #close button on about us
    def test_close_button(self, driver):
        driver.get(url)
        time.sleep(2)
        about_us = driver.find_element(By.CSS_SELECTOR, about_us_val)
        about_us.click()
        time.sleep(1)

        close_button = driver.find_element(By.CSS_SELECTOR, "#videoModal > div > div > div.modal-footer > button")

        assert close_button.is_displayed(), "Close button is not visible"
        assert close_button.is_enabled(), "Close button is not clickable"

        close_button.click()
        time.sleep(1)