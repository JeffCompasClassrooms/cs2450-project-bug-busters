from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

# Path to your ChromeDriver
chrome_driver_path = r"C:\Users\rlmee\Downloads\unit testing\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# Initialize WebDriver with Service
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Base URL of your Flask app
BASE_URL = "http://localhost:5000"

# Test credentials
TEST_USERNAME = "test123"
TEST_PASSWORD = "test123"

def wait_for_element(by, value, timeout=5):
    """Helper function to wait for an element to be visible."""
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by, value)))

try:
    print("--= Beginning Tests =--")

    # Open Login Page
    driver.get(f"{BASE_URL}/loginscreen")
    
    # Ensure login form loads
    wait_for_element(By.TAG_NAME, "form")
    print("[PASSED] - Login form is displayed.")

    # Test Case 1: Check if login button exists
    login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Login']")
    assert login_button is not None, "[FAILED] - Login button not found."
    print("[PASSED] - Login button exists.")

    # Test Case 2: Attempt login with empty fields
    login_button.click()
    time.sleep(1)
    assert driver.current_url == f"{BASE_URL}/loginscreen", "[FAILED] - Login should fail with empty fields."
    print("[PASSED] - Login fails with empty fields.")

    # Test Case 3: Attempt login with incorrect credentials
    driver.get(f"{BASE_URL}/loginscreen")
    wait_for_element(By.NAME, "username").send_keys("wronguser")
    wait_for_element(By.NAME, "password").send_keys("wrongpass")
    login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Login']")
    login_button.click()
    time.sleep(1)
    assert driver.current_url == f"{BASE_URL}/loginscreen", "[FAILED] - Login should fail with incorrect credentials."
    print("[PASSED] - Login fails with incorrect credentials.")

    # Test Case 4: Attempt login with correct credentials
    driver.get(f"{BASE_URL}/loginscreen")
    wait_for_element(By.NAME, "username").send_keys(TEST_USERNAME)
    wait_for_element(By.NAME, "password").send_keys(TEST_PASSWORD)
    login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Login']")
    login_button.click()
    time.sleep(1)
    assert driver.current_url == f"{BASE_URL}/", "[FAILED] - Login did not redirect to main page."
    print("[PASSED] - Login succeeds with correct credentials.")

    # Test Case 5: Check if user is remembered with cookies
    username_cookie = driver.get_cookie("username")
    assert username_cookie and username_cookie['value'] == TEST_USERNAME, "[FAILED] - Username cookie not set correctly."
    print("[PASSED] - Username cookie is set correctly.")

    # Test Case 6: Logout functionality
    try:
        logout_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "form[action='/logout'] button[name='logout']"))
        )
        logout_button.click()
        time.sleep(1)
        assert driver.current_url == f"{BASE_URL}/loginscreen", "[FAILED] - Logout failed."
        print("[PASSED] - Logout works correctly.")
    except TimeoutException:
        print("[ERROR] - Logout button not found. User might not be logged in.")

    # Test Case 7: Ensure username cookie is removed after logout
    username_cookie = driver.get_cookie("username")
    assert username_cookie is None, "[FAILED] - Username cookie was not removed after logout."
    print("[PASSED] - Username cookie is removed after logout.")

    # Test Case 8: Check the "Create" account button appears when clicked
    driver.get(f"{BASE_URL}/loginscreen")
    create_link = driver.find_element(By.LINK_TEXT, "Click here")
    create_link.click()
    create_button = wait_for_element(By.ID, "create-btn")
    assert create_button.is_displayed(), "[FAILED] - Create button did not appear."
    print("[PASSED] - Create button appears when clicked.")

    # Test Case 9: Ensure password field is hidden
    password_field = driver.find_element(By.NAME, "password")
    assert password_field.get_attribute("type") == "password", "[FAILED] - Password field is not secure."
    print("[PASSED] - Password field is of type 'password'.")

    # Test Case 10: Ensure page title is correct
    assert "BetBrawl" in driver.title, "[FAILED] - Page title is wrong."
    print("[PASSED] - page title is correct.")

except Exception as e:
    print("[ERROR] Test execution failed:", e)

finally:
    print("--= Ending Tests =--")
    driver.quit()
