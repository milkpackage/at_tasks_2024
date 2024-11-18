from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

about_us_val = "#navbarExample > ul > li:nth-child(3) > a"
url = 'https://www.demoblaze.com/'


class TestAboutUs:
    def test_about_us_button(self, driver):
        driver.get(url)
        time.sleep(2)

        about_us = driver.find_element(By.CSS_SELECTOR, about_us_val)
        assert about_us.is_displayed(), "About Us is not visible"
        assert about_us.is_enabled(), "About Us is not clickable"
        about_us.click()
        time.sleep(1)

    def test_video_player(self, driver):
        driver.get(url)
        time.sleep(2)
        about_us = driver.find_element(By.CSS_SELECTOR, about_us_val)
        about_us.click()
        time.sleep(1)

        video_element = driver.find_element(By.CLASS_NAME, "vjs-poster")
        assert video_element.is_displayed(), "Video elements are not visible"
        video_element.click()
        time.sleep(2)

    def test_close_button(self, driver):
        try:
            driver.get(url)
            time.sleep(2)
            about_us = driver.find_element(By.CSS_SELECTOR, about_us_val)
            about_us.click()
            time.sleep(1)

            # failing test to record
            close_button = driver.find_element(By.XPATH, "#videoModal > div > div > div.modal-footer > button")

            if not close_button.is_displayed():
                raise AssertionError("Close button is not visible")
            if not close_button.is_enabled():
                raise AssertionError("Close button is not clickable")

            close_button.click()
            time.sleep(1)

        except (NoSuchElementException, AssertionError) as e:
            time.sleep(5)
            raise