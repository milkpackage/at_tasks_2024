from page_objects.bug_report_page import BugReportPage
import logging

logger = logging.getLogger(__name__)


class BugReportBO:
    def __init__(self, driver):
        self.bug_report_page = BugReportPage(driver)
        self.driver = driver

    def create_bug(self, summary: str, description: str, **kwargs) -> bool:
        try:
            self.bug_report_page.create_bug(summary, description, **kwargs)
            logger.debug(f"Current URL after bug creation: {self.driver.current_url}")
            logger.debug(f"Page source after bug creation: {self.driver.page_source[:500]}")
            return summary in self.driver.page_source
        except Exception as e:
            logger.error(f"Failed to create bug: {str(e)}")
            return False