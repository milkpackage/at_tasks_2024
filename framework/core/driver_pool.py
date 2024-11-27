from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from typing import Dict
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
    
    def _create_driver(self, browser_type: str) -> WebDriver:
        """Create a new WebDriver instance with the specified browser type"""
        browser_type = browser_type.lower()
        
        if browser_type == "chrome":
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service)
        elif browser_type == "firefox":
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service)
        else:
            raise ValueError(f"Unsupported browser type: {browser_type}")
            
        driver.maximize_window()
        return driver

    def get_driver(self, browser_type: str = "chrome") -> WebDriver:
        #get or create driver
        thread_id = str(threading.current_thread().ident)
        key = f"{browser_type}_{thread_id}"
        
        if key not in self._drivers:
            self._drivers[key] = self._create_driver(browser_type)
        
        return self._drivers[key]
    
    def quit_driver(self, browser_type: str = None):
        #quit specific driver or quit all drivers
        thread_id = str(threading.current_thread().ident)
        
        if browser_type:
            key = f"{browser_type}_{thread_id}"
            if key in self._drivers:
                self._drivers[key].quit()
                del self._drivers[key]
        else:
            #quit all drivers for current thread
            for key in list(self._drivers.keys()):
                if key.endswith(thread_id):
                    self._drivers[key].quit()
                    del self._drivers[key]

    def quit_all(self):
        for driver in self._drivers.values():
            driver.quit()
        self._drivers.clear()