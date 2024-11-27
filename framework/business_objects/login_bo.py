from page_objects.login_page import LoginPage

class LoginBO:
    def __init__(self, driver):
        self.login_page = LoginPage(driver)
    
    def login(self, username: str, password: str) -> bool:
        self.login_page.open()
        self.login_page.login(username, password)
        return "My View" in self.login_page.driver.title