#pytest test_booking.py -v -s

# test_booking.py
import logging
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from page_factory import PageFactory
import time

# adding logger config
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@pytest.fixture(autouse=True)
def setup_logging(caplog):
    caplog.set_level(logging.INFO)

class BookingPage:
    def __init__(self, driver):
        self.driver = driver
        self.factory = PageFactory(self.driver)

        # initializing element via page folder
        self.currency_button = self.factory.get_dropdown(
            (By.CSS_SELECTOR, "button[data-testid='header-currency-picker-trigger']")
        )

        self.language_button = self.factory.get_dropdown(
            (By.CSS_SELECTOR, "button[data-testid='header-language-picker-trigger']")
        )

        self.occupancy_button = self.factory.get_dropdown(
            (By.CSS_SELECTOR, "button[data-testid='occupancy-config']")
        )
    # to close pop-up which shows with site launch with click
    def dismiss_popup(self):
        logger.info("Dismissing with click")
        ActionChains(self.driver).click().perform()
        time.sleep(1)
        return self

    def change_currency(self, currency):
        logger.info(f"Changing currency to: {currency}")
        self.currency_button.select_by_text(currency)
        return self

    def change_language(self, language):
        logger.info(f"Changing language to: {language}")
        self.language_button.select_by_text(language)
        return self

    def select_occupancy(self, adults):
        logger.info(f"Setting adults number to: {adults}")
        self.occupancy_button.select_by_text(adults)
        return self


def test_booking_dropdowns(caplog):
    logger.info("Starting test")

    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-notifications')

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        booking = BookingPage(driver)
        logger.info("Page initialized")

        driver.get("https://www.booking.com")
        time.sleep(2)
        logger.info("Navigated to booking.com")

        booking.dismiss_popup()

        booking.change_currency("EUR")
        time.sleep(2)

        booking.select_occupancy("2 adults")
        time.sleep(2)

        booking.change_language("Українська")
        time.sleep(2)

        logger.info("Test completed successfully!")

    finally:
        driver.quit()


if __name__ == "__main__":
    pytest.main(["-v -s"])