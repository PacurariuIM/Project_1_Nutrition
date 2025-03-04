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

def test_form_submission(driver, app_url):
    """Test submitting the ingredients form and getting recipes."""
    print("\nStarting form submission test...")
    driver.get(app_url)
    print(f"Current URL: {driver.current_url}")
    
    # Find and fill the ingredients input
    ingredients_input = wait_and_log(driver, (By.ID, "ingredients"))
    ingredients_input.send_keys("chicken, rice")
    print("Entered ingredients")
    
    # Submit the form
    ingredients_input.send_keys(Keys.RETURN)
    print("Submitted form")
    
    # Wait for and verify recipe results appear
    recipe_cards = wait_and_log(driver, (By.CLASS_NAME, "recipe-card"), timeout=60)
    print("Found recipe cards")
    
    # Additional debugging
    print(f"Page title: {driver.title}")
    print(f"Current URL after search: {driver.current_url}")

def test_form_submission_no_results(driver, app_url):
    """Test submitting the form with ingredients that return no results."""
    driver.get(app_url)
    
    ingredients_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ingredients"))
    )
    ingredients_input.send_keys("zzzzzz, xxxxxx")
    ingredients_input.send_keys(Keys.RETURN)
    
    # Look for the error message text instead of alert-danger class
    error_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-center"))
    )
    assert "No recipes to display" in error_message.text

def test_recipe_detail_navigation(driver, app_url):
    """Test clicking a recipe card navigates to recipe details."""
    driver.get(app_url)
    ingredients_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ingredients"))
    )
    ingredients_input.send_keys("chicken, rice")
    ingredients_input.send_keys(Keys.RETURN)
    
    # Wait for recipe cards and click the first one
    recipe_card = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "recipe-card"))
    )
    recipe_card.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # Verify recipe detail page elements using the correct classes
    recipe_title = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "my-5"))
    )
    ingredients_list = driver.find_element(By.CLASS_NAME, "list-group")
    instructions_list = driver.find_element(By.CLASS_NAME, "list-group-numbered")
    
    assert recipe_title is not None
    assert ingredients_list is not None
    assert instructions_list is not None 