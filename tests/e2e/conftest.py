import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

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
    
    # Minimal required options for CI
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--incognito')
    
    # Setup Chrome WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(30)
    
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def app_url(request):
    """Get the application URL from command line options."""
    return request.config.getoption("--app-url")

# Add a helper function for debugging
def wait_and_log(driver, locator, timeout=30):
    """Wait for element and log if not found."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        print(f"Found element: {locator}")
        return element
    except Exception as e:
        print(f"Failed to find element: {locator}")
        print(f"Page source: {driver.page_source}")
        raise e

def pytest_configure(config):
    """Set up test environment."""
    os.environ['FLASK_ENV'] = 'development'

@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """Setup test environment variables."""
    old_env = os.environ.get('FLASK_ENV')
    os.environ['FLASK_ENV'] = 'development'
    yield
    if old_env:
        os.environ['FLASK_ENV'] = old_env
    else:
        del os.environ['FLASK_ENV']