import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode"
    )
    parser.addoption(
        "--app-url",
        action="store",
        default="http://127.0.0.1:5000",
        help="Application URL for testing"
    )

@pytest.fixture(scope="session")
def driver(request):
    """Create a WebDriver instance that can be used for all tests."""
    chrome_options = Options()
    # Add headless option for CI environment
    if request.config.getoption("--headless"):
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Add these lines to suppress the errors:
    chrome_options.add_argument('--log-level=3')  # Only show fatal errors
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    # Setup Chrome WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)  # seconds
    
    yield driver
    
    # Quit the driver after all tests are done
    driver.quit()

@pytest.fixture(scope="session")
def app_url(request):
    """Get the application URL from command line options."""
    return request.config.getoption("--app-url") 