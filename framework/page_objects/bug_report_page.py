from selenium.webdriver.common.by import By
from core.web_element_wrapper import Element
from page_objects.base_page import BasePage
import logging

logger = logging.getLogger(__name__)

class BugReportPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost/bug_report_page.php"
        
        #form elements
        self.category_select = Element(driver, By.NAME, "category_id")
        self.reproducibility_select = Element(driver, By.NAME, "reproducibility")
        self.severity_select = Element(driver, By.NAME, "severity")
        self.priority_select = Element(driver, By.NAME, "priority")
        self.summary_input = Element(driver, By.NAME, "summary")
        self.description_textarea = Element(driver, By.NAME, "description")
        self.submit_button = Element(driver, By.CSS_SELECTOR, "input[type='submit']")

    def create_bug(self, summary, description, category="General", 
                  reproducibility="always", severity="minor", priority="normal"):
        logger.debug(f"Creating bug with summary: {summary}")
        try:
            self.driver.get(self.url)
            
            #form filling
            logger.debug("Filling in bug report form...")
            self.category_select.select_by_value(category)  
            self.reproducibility_select.select_by_value(reproducibility)
            self.severity_select.select_by_value(severity)
            self.priority_select.select_by_value(priority)
            
            self.summary_input.send_keys(summary)
            self.description_textarea.send_keys(description)
            
            logger.debug("Submitting bug report...")
            self.submit_button.click()
            return True
            
        except Exception as e:
            logger.error(f"Failed to create bug: {str(e)}")
            return False

    def is_bug_created_successfully(self):
        try:
            success_message = Element(self.driver, By.CLASS_NAME, "alert-success")
            return success_message.is_displayed()
        except:
            return False