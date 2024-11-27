import pytest
from business_objects.login_bo import LoginBO
from business_objects.bug_report_bo import BugReportBO
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

@pytest.fixture(scope="function")
def logged_in_driver(driver):
    login_bo = LoginBO(driver)
    login_bo.login("administrator", "admin")  #change here to your data if needed
    return driver

def test_create_simple_bug(logged_in_driver):
    try:
        bug_report_bo = BugReportBO(logged_in_driver)
        result = bug_report_bo.create_bug(
            summary="Testing",
            description="Test created by framework"
        )
        assert result is True
        
    except Exception as e:
        logger.error(f"Test failed with error: {str(e)}")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"test_failure_{timestamp}.png"
        logged_in_driver.save_screenshot(screenshot_path)
        logger.error(f"Screenshot saved to {screenshot_path}")
        raise

def test_create_bug_with_all_fields(logged_in_driver):
    try:
        bug_report_bo = BugReportBO(logged_in_driver)
        result = bug_report_bo.create_bug(
            summary="Full Test",
            description="All fields",
            category="1",  
            reproducibility="10",  
            severity="50",  
            priority="30"  
        )
        assert result is True
        
    except Exception as e:
        logger.error(f"Test failed with error: {str(e)}")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"test_failure_{timestamp}.png"
        logged_in_driver.save_screenshot(screenshot_path)
        logger.error(f"Screenshot saved to {screenshot_path}")
        raise