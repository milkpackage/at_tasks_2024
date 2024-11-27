import pytest
import logging
from business_objects.login_bo import LoginBO
from datetime import datetime

logger = logging.getLogger(__name__)

def test_login(driver):
    try:
        logger.debug("Starting login test")
        driver.get("http://localhost/")
        logger.debug(f"Current URL: {driver.current_url}")
        logger.debug("Page source:")
        logger.debug(driver.page_source)
        
        login_bo = LoginBO(driver)
        result = login_bo.login("administrator", "admin")
        assert result is True
        
    except Exception as e:
        logger.error(f"Test failed with error: {str(e)}")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"test_failure_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        logger.error(f"Screenshot saved to {screenshot_path}")
        raise