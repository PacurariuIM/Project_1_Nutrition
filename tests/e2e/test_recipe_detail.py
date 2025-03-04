from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

def test_recipe_unit_converter(driver, app_url):
    """Test the unit converter functionality on recipe detail page."""
    # Navigate to a recipe detail page (reusing navigation from previous test)
    driver.get(app_url)
    ingredients_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ingredients"))
    )
    ingredients_input.send_keys("chicken")
    ingredients_input.send_keys(Keys.RETURN)
    
    # Click first recipe
    recipe_card = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "recipe-card"))
    )
    recipe_card.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # Test unit converter
    input_value = driver.find_element(By.ID, "inputValue")
    input_value.send_keys("100")
    
    # Select conversion units
    from_unit = Select(driver.find_element(By.ID, "fromUnit"))
    from_unit.select_by_value("g")
    
    to_unit = Select(driver.find_element(By.ID, "toUnit"))
    to_unit.select_by_value("oz")
    
    # Click convert
    driver.find_element(By.XPATH, "//button[text()='Convert']").click()
    
    # Verify result appears
    result = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "resultBox"))
    )
    assert result.text != "", "Conversion result should not be empty"

def test_pdf_download(driver, app_url):
    """Test the PDF download functionality on recipe detail page."""
    # Navigate to a recipe detail page
    driver.get(app_url)
    ingredients_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ingredients"))
    )
    ingredients_input.send_keys("chicken")
    ingredients_input.send_keys(Keys.RETURN)
    
    # Click first recipe
    recipe_card = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "recipe-card"))
    )
    recipe_card.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # Find and click the download PDF button
    download_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "downloadPdf"))
    )
    
    # Verify button styling
    button_color = download_button.value_of_css_property("background-color")
    assert button_color in ["rgb(139, 0, 0)", "#8b0000", "rgba(139, 0, 0, 1)"], "PDF button should be dark red"
    
    # Verify button is clickable
    assert download_button.is_enabled(), "Download PDF button should be enabled"

def test_back_button_navigation(driver, app_url):
    """Test the back button navigation from recipe detail page."""
    # Navigate to a recipe detail page first
    driver.get(app_url)
    ingredients_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ingredients"))
    )
    ingredients_input.send_keys("chicken")
    ingredients_input.send_keys(Keys.RETURN)
    
    # Store the recipes page URL
    recipes_page_url = driver.current_url
    
    # Click first recipe
    recipe_card = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "recipe-card"))
    )
    recipe_card.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # Find and click the back button
    back_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn-secondary"))
    )
    back_button.click()
    
    # Verify we're back on the recipes page
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "recipe-card"))
    )
    assert driver.current_url == recipes_page_url, "Should return to recipes page" 