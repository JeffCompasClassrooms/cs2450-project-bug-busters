from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Correct ChromeDriver path
chrome_driver_path = r"C:\Users\bryso\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# Use Service object
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

try:
    driver.get("http://localhost:5000/loginscreen")
    time.sleep(2)

    print("--= Beginning Tests =--")

    # Test for login button
    try:
        login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Login']")
        print("[PASSED] - Login Button Exists.")
    except Exception:
        print("[FAILED] - Login button not found.")

    # Test for dark mode button
    try:
        dark_mode_button = driver.find_element(By.ID, "darkModeToggle")
        print("[PASSED] - Dark Mode Button Exists.")
    except Exception:
        print("[FAILED] - Dark Mode button not found.")

    # Dark Mode functionality test
    print("--= Testing Dark Mode Functionality =--")
    try:
        dark_mode_button.click()
        time.sleep(1)
        body_element = driver.find_element(By.TAG_NAME, "body")
        if "dark-mode" in body_element.get_attribute("class"):
            print("[PASSED] - Dark Mode Enabled Successfully.")
        else:
            print("[FAILED] - Dark Mode did not enable.")
    except Exception as e:
        print("[FAILED] - Error while testing Dark Mode:", e)

    # Test for leaderboard link
    try:
        leaderboard_link = driver.find_element(By.LINK_TEXT, "Leaderboard")
        print("[PASSED] - Leaderboard Link Exists.")
    except Exception:
        print("[FAILED] - Leaderboard link not found.")

    # Test for casino link
    try:
        casino_link = driver.find_element(By.LINK_TEXT, "Casino")
        print("[PASSED] - Casino Link Exists.")
    except Exception:
        print("[FAILED] - Casino link not found.")

    # Test for social link
    try:
        social_link = driver.find_element(By.LINK_TEXT, "Social")
        print("[PASSED] - Social Link Exists.")
    except Exception:
        print("[FAILED] - Social link not found.")

    # Test for Create button
    try:
        create_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Create']")
        print("[PASSED] - Create Button Exists.")
    except Exception:
        print("[FAILED] - Create button not found.")

    # Test for Username input field
    try:
        username_input = driver.find_element(By.NAME, "username")
        print("[PASSED] - Username Input Field Exists.")
    except Exception:
        print("[FAILED] - Username input field not found.")

    # Test for Password input field
    try:
        password_input = driver.find_element(By.NAME, "password")
        print("[PASSED] - Password Input Field Exists.")
    except Exception:
        print("[FAILED] - Password input field not found.")

     # Test that username and password fields accept input
    try:
        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")

        username_input.clear()
        password_input.clear()

        username_input.send_keys("test_user")
        password_input.send_keys("test_pass")

        # Verify that the values were entered correctly
        if username_input.get_attribute("value") == "test_user" and password_input.get_attribute("value") == "test_pass":
            print("[PASSED] - Input Fields Accept Text.")
        else:
            print("[FAILED] - Text not properly entered in input fields.")
    except Exception:
        print("[FAILED] - Could not test input field behavior.")

except Exception as e:
    print("Error:", e)

finally:
    print("--= Ending Tests =--")
    driver.quit()
