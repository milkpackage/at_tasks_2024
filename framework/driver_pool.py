from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Dict, Optional
import threading
from threading import Lock


class DriverPool:
    _instance = None
    _lock = Lock()
    _drivers: Dict[str, WebDriver] = {}

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def get_driver(self, browser_type: str = "chrome") -> WebDriver:
        thread_id = str(threading.current_thread().ident)
        key = f"{browser_type}_{thread_id}"

        if key not in self._drivers:
            if browser_type.lower() == "chrome":
                self._drivers[key] = webdriver.Chrome()
            elif browser_type.lower() == "firefox":
                self._drivers[key] = webdriver.Firefox()
            else:
                raise ValueError(f"Unsupported browser type: {browser_type}")

            self._drivers[key].maximize_window()

        return self._drivers[key]

    def quit_all(self):
        for driver in self._drivers.values():
            driver.quit()
        self._drivers.clear()