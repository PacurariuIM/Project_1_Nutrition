from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from tests.e2e.conftest import wait_and_log

def test_home_page_loads(driver, app_url):
    """Test that the home page loads and contains the expected form."""
    # Navigate to the home page
    driver.get(app_url)
    
    # Wait for and verify the form is present
    form = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "form"))
    )
    assert form is not None
    
    # Check for the ingredients input field
    ingredients_input = driver.find_element(By.ID, "ingredients")
    assert ingredients_input is not None
    
    # Verify the submit button exists
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    assert submit_button is not None 