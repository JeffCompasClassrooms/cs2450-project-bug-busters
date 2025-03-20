from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Correct ChromeDriver path
chrome_driver_path = r"C:\Users\bryso\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# Use Service object
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)  # ✅ Correct way to initialize Chrome WebDriver

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

except Exception as e:
    print("Error:", e)

finally:
    print("--= Ending Tests =--")
    driver.quit()
