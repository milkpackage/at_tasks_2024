import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class AndroidCalculatorTest(unittest.TestCase):
    def setUp(self):
        options = UiAutomator2Options()
        options.platform_name = 'Android'
        options.platform_version = '15'
        options.device_name = 'emulator-5554'
        options.automation_name = 'UiAutomator2'
        options.app_package = 'com.google.android.calculator'
        options.app_activity = 'com.android.calculator2.Calculator'

        self.driver = webdriver.Remote('http://localhost:4725', options=options)
        self.wait = WebDriverWait(self.driver, 10)
        print("Test setup completed")

    def test_invalid_input(self):
        try:
            print("\nTest Case 1: Testing letters input")

            formula_field = self.wait.until(
                EC.presence_of_element_located((AppiumBy.ID, "com.google.android.calculator:id/formula"))
            )
            test_input = "abc"
            formula_field.send_keys(test_input)
            time.sleep(1)

            print(f"Entered text: {formula_field.text}")

            self.driver.get_screenshot_as_file("letters_before_equals.png")
            with open("letters_before_equals_dom.xml", "w") as f:
                f.write(self.driver.page_source)

            equals_button = self.wait.until(
                EC.presence_of_element_located((AppiumBy.ID, "com.google.android.calculator:id/eq"))
            )
            equals_button.click()
            time.sleep(1)

            self.driver.get_screenshot_as_file("letters_after_equals.png")
            with open("letters_after_equals_dom.xml", "w") as f:
                f.write(self.driver.page_source)

            formula = self.wait.until(
                EC.presence_of_element_located((AppiumBy.ID, "com.google.android.calculator:id/formula"))
            )
            result = self.wait.until(
                EC.presence_of_element_located((AppiumBy.ID, "com.google.android.calculator:id/result_preview"))
            )

            print(f"Formula text: {formula.text}")
            print(f"Result text: {result.text}")

            error_present = False
            try:
                error_msg = self.driver.find_element(AppiumBy.ID, "com.google.android.calculator:id/result_preview")
                error_present = "Format error" in error_msg.text or error_msg.text == ""
            except:
                pass

            self.assertTrue(error_present, "Calculator should show format error or empty result for invalid input")

            delete_button = self.wait.until(
                EC.presence_of_element_located((AppiumBy.ID, "com.google.android.calculator:id/del"))
            )
            for _ in range(len(test_input)):
                delete_button.click()
                time.sleep(0.5)

            print("\nTest Case 2: Testing symbols input")
            test_input = "@#$"
            formula_field.send_keys(test_input)
            time.sleep(1)

            self.driver.get_screenshot_as_file("symbols_before_equals.png")
            with open("symbols_before_equals_dom.xml", "w") as f:
                f.write(self.driver.page_source)

            equals_button.click()
            time.sleep(1)

            self.driver.get_screenshot_as_file("symbols_after_equals.png")
            with open("symbols_after_equals_dom.xml", "w") as f:
                f.write(self.driver.page_source)

            formula = self.driver.find_element(AppiumBy.ID, "com.google.android.calculator:id/formula")
            result = self.driver.find_element(AppiumBy.ID, "com.google.android.calculator:id/result_preview")

            print(f"Formula text: {formula.text}")
            print(f"Result text: {result.text}")

            error_present = False
            try:
                error_msg = self.driver.find_element(AppiumBy.ID, "com.google.android.calculator:id/result_preview")
                error_present = "Format error" in error_msg.text or error_msg.text == ""
            except:
                pass

            self.assertTrue(error_present, "Calculator should show format error or empty result for invalid input")

        except Exception as e:
            print(f"\nTest failed: {str(e)}")
            self.driver.get_screenshot_as_file("test_failure.png")
            with open("failure_dom.xml", "w") as f:
                f.write(self.driver.page_source)
            raise e

    def tearDown(self):
        if self.driver:
            self.driver.quit()


if __name__ == '__main__':
    unittest.main()