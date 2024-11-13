from selenium.webdriver.common.by import By
from main_page import MainPage

class AboutUsPage(MainPage):
    VIDEO_PLAYER = (By.CLASS_NAME, "vjs-poster")
    CLOSE_BUTTON = (By.CSS_SELECTOR, "#videoModal > div > div > div.modal-footer > button")
    VIDEO_MODAL = (By.ID, "videoModal")

    def play_video(self):
        self.click_element(self.VIDEO_PLAYER)
        return self

    def close_video(self):
        self.click_element(self.CLOSE_BUTTON)
        return self

    def is_video_modal_open(self):
        return self.is_element_visible(self.VIDEO_MODAL)