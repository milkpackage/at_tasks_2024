from page_objects.bug_report_page import BugReportPage
import logging

logger = logging.getLogger(__name__)

class BugReportBO:
    def __init__(self, driver):
        self.bug_report_page = BugReportPage(driver)
    
    def create_bug(self, summary: str, description: str, **kwargs) -> bool:
        try:
            self.bug_report_page.create_bug(summary, description, **kwargs)
            return self.bug_report_page.is_bug_created_successfully()
        except Exception as e:
            logger.error(f"Failed to create bug: {str(e)}")
            return False