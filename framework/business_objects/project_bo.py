from page_objects.project_page import ProjectPage
import logging

logger = logging.getLogger(__name__)


class ProjectBO:
    def __init__(self, driver):
        self.project_page = ProjectPage(driver)

    def create_project(self, name: str, **kwargs) -> bool:
        try:
            return self.project_page.create_project(name, **kwargs)
        except Exception as e:
            logger.error(f"Failed to create project: {str(e)}")
            return False