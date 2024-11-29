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

        login_bo = LoginBO(driver)
        result = login_bo.login("administrator", "admin")  # Use correct password

        # Add multiple verification points
        assert result is True, "Login verification failed"
        assert "administrator" in driver.page_source, "Username not found in page"
        assert "logout" in driver.page_source.lower(), "Logout link not found"

    except Exception as e:
        logger.error(f"Test failed with error: {str(e)}")
        screenshot_path = "login_failure.png"
        driver.save_screenshot(screenshot_path)
        logger.error(f"Screenshot saved to {screenshot_path}")
        raise