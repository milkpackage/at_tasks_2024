import pytest
from driver_pool import DriverPool

@pytest.fixture(scope="function")
def driver(request):
    browser = request.config.getoption("--browser", default="chrome")
    driver_pool = DriverPool()
    driver = driver_pool.get_driver(browser)
    yield driver
    driver.wait(5)
    driver_pool.quit_all()

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                    help="browser to execute tests (chrome or firefox)")