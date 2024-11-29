import pytest
from business_objects.project_bo import ProjectBO
from business_objects.login_bo import LoginBO

@pytest.fixture(scope="function")
def logged_in_driver(driver):
    login_bo = LoginBO(driver)
    login_bo.login("administrator", "admin")  #change here to your data if needed
    return driver

def test_create_project(logged_in_driver):
    project_name = "Test Project"
    project_bo = ProjectBO(logged_in_driver)
    result = project_bo.create_project(
        name=project_name,
        description="Test project created by framework",
        status="development",
        view_status="public"
    )
    assert result is True
    assert project_name in logged_in_driver.page_source