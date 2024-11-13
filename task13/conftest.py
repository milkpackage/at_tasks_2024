import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
from datetime import datetime
import threading
import time
from utils import CustomLogger, VideoRecorder, ResultStorage

Path('logs').mkdir(exist_ok=True)
Path('video_records').mkdir(exist_ok=True)
Path('failed_tests_html').mkdir(exist_ok=True)

logger = CustomLogger()
video_recorder = VideoRecorder()
result_storage = ResultStorage()


def start_recording_thread(video_recorder, test_name):
    #running recording on separate thread
    video_recorder.start_recording(test_name)
    start_time = time.time()
    while video_recorder.recording and (time.time() - start_time) < 5:
        video_recorder.capture_frame()
        time.sleep(0.1)


@pytest.fixture(scope="function")
def driver(request):
    print("\nLaunching Chrome browser...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()

    if hasattr(request, 'node') and hasattr(request.node, 'cls'):
        request.node.cls.driver = driver

    yield driver

    #adding delay to keep browser open
    if hasattr(request, 'node'):
        report = getattr(request.node, 'report', None)
        if report and report.failed:
            time.sleep(5)

    print("\nClosing Chrome browser...")
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # saving report
    if hasattr(item, 'node'):
        item.node.report = report

    if report.when == "call":
        if report.failed:
            logger.logger.error(f"Test failed: {item.name}")

            recording_thread = threading.Thread(
                target=start_recording_thread,
                args=(video_recorder, item.name)
            )
            recording_thread.daemon = True
            recording_thread.start()

            # saving html
            if hasattr(item, 'funcargs') and 'driver' in item.funcargs:
                driver = item.funcargs['driver']
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                html_path = f'failed_tests_html/{item.name}_{timestamp}.html'

                try:
                    with open(html_path, 'w', encoding='utf-8') as f:
                        f.write(driver.page_source)
                    logger.logger.info(f"HTML source saved to: {html_path}")

                    time.sleep(5)
                except Exception as e:
                    logger.logger.error(f"Failed to save HTML source: {e}")

            #waiting for video
            recording_thread.join(timeout=6)
            video_recorder.stop_recording()
            logger.logger.info(f"Video recorded for failed test: {item.name}")

        result_storage.add_result(
            item.name,
            "passed" if report.passed else "failed" if report.failed else "skipped",
            {"outcome": report.outcome}
        )


def pytest_sessionfinish(session):
    logger.logger.info("Test session finished")
    if video_recorder.recording:
        video_recorder.stop_recording()