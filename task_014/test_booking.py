from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from page_factory import PageFactory
from video_recorder import VideoRecorder
import time
from datetime import datetime
import os
import logging
import pytest
import allure


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

    @allure.step("Dismissing popup")
    def dismiss_popup(self):
        logger.info("Dismissing with click")
        ActionChains(self.driver).click().perform()
        time.sleep(1)
        return self

    @allure.step("Changing currency to {currency}")
    def change_currency(self, currency):
        logger.info(f"Changing currency to: {currency}")
        self.currency_button.select_by_text(currency)
        return self

    @allure.step("Changing language to {language}")
    def change_language(self, language):
        logger.info(f"Changing language to: {language}")
        self.language_button.select_by_text(language)
        return self

    @allure.step("Setting adults number to {adults}")
    def select_occupancy(self, adults):
        logger.info(f"Setting adults number to: {adults}")
        self.occupancy_button.select_by_text(adults)
        return self

@pytest.fixture
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-notifications')

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    video_recorder = VideoRecorder()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_path = f"videos/test_recording_{timestamp}.mp4"
    os.makedirs("videos", exist_ok=True)

    def record_video():
        video_recorder.start_recording(video_path)
        while video_recorder.recording:
            video_recorder.capture_frame()
            time.sleep(0.1)

    import threading
    recording_thread = threading.Thread(target=record_video)
    recording_thread.daemon = True
    recording_thread.start()

    setattr(driver, 'video_recorder', video_recorder)

    def finalizer():
        try:

            video_recorder.recording = False
            recording_thread.join(timeout=1)
            video_recorder.stop_recording()

            time.sleep(1)

            if os.path.exists(video_path):
                allure.attach.file(
                    video_path,
                    name=f"test_video_{timestamp}",
                    attachment_type=allure.attachment_type.MP4
                )
                logger.info(f"Video attached to Allure report: {video_path}")
            else:
                logger.error(f"Video file not found: {video_path}")

        except Exception as e:
            logger.error(f"Failed to attach video: {e}")
        finally:
            driver.quit()

    request.addfinalizer(finalizer)
    return driver


@allure.feature("Booking.com Interface")
@allure.story("Dropdown Functionality")
@allure.title("Test Currency, Language and Occupancy Dropdowns")
def test_booking_dropdowns(driver, caplog):
    try:
        with allure.step("Starting test"):
            logger.info("Starting test")
            booking = BookingPage(driver)

        with allure.step("Navigating to booking.com"):
            driver.get("https://www.booking.com")
            time.sleep(2)
            logger.info("Navigated to booking.com")

        # capture initial state
        allure.attach(
            driver.get_screenshot_as_png(),
            name="initial_state",
            attachment_type=allure.attachment_type.PNG
        )
        allure.attach(
            driver.page_source,
            name="initial_page_source",
            attachment_type=allure.attachment_type.HTML
        )

        booking.dismiss_popup()

        with allure.step("Testing currency dropdown"):
            booking.change_currency("EUR")
            time.sleep(2)
            driver.video_recorder.capture_frame()

        with allure.step("Testing occupancy dropdown"):
            booking.select_occupancy("2 adults")
            time.sleep(2)
            driver.video_recorder.capture_frame()

        with allure.step("Testing language dropdown"):
            booking.change_language("Українська")
            time.sleep(2)
            driver.video_recorder.capture_frame()

        allure.attach(
            driver.get_screenshot_as_png(),
            name="final_state",
            attachment_type=allure.attachment_type.PNG
        )
        allure.attach(
            driver.page_source,
            name="final_page_source",
            attachment_type=allure.attachment_type.HTML
        )

        logger.info("Test completed successfully!")

    except Exception as e:

        allure.attach(
            driver.get_screenshot_as_png(),
            name="failure_screenshot",
            attachment_type=allure.attachment_type.PNG
        )
        allure.attach(
            driver.page_source,
            name="failure_page_source",
            attachment_type=allure.attachment_type.HTML
        )
        logger.error(f"Test failed: {str(e)}")
        raise


if __name__ == "__main__":
    pytest.main(["-v", "-s", "--alluredir=./allure-results"])