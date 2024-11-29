import pytest
from core.driver_pool import DriverPool

@pytest.fixture(scope="function")
def driver(request):
    browser = request.config.getoption("--browser", default="chrome")
    driver_pool = DriverPool()
    driver = driver_pool.get_driver(browser)
    yield driver
    driver_pool.quit_driver(browser)

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                    help="Browser for testing (chrome or firefox)")



