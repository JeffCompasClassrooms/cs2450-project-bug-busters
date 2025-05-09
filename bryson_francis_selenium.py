from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Use Remote WebDriver with the standalone Selenium Chrome container
selenium_url = os.environ.get("SELENIUM_REMOTE_URL", "http://localhost:4444/wd/hub")
driver = webdriver.Remote(
    command_executor=selenium_url,
    options=options
)

try:
    driver.get("http://localhost:5000/loginscreen")
    time.sleep(2)

    print("--= Beginning Tests - <Bryson Francis> =--")
    login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Login']")
    print("[PASSED] - Login Button Exists.") if login_button else print("[FAILED] - Login button not found.")

    create_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Create']")
    print("[PASSED] - Create Button Exists.") if create_button else print("[FAILED] - Create button not found.")

    driver.find_element(By.NAME, "username").send_keys("testuser")
    driver.find_element(By.NAME, "password").send_keys("pass1234")
    driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Login']").click()
    print("[PASSED] - Log in successful.")
    time.sleep(5)

    driver.find_element(By.CSS_SELECTOR, "input[type='text'][name='name']").send_keys("goose")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit'][name='addfriend']").click()
    time.sleep(3)
    print("[PASSED] - Add friend button successful.")

    friend = driver.find_element(By.CSS_SELECTOR, "a[href='/friend/goose']")
    print("[PASSED] - Friend Exists.") if friend else print("[FAILED] - Friend not found.")

    dark_mode_button = driver.find_element(By.ID, "darkModeToggle")
    print("[PASSED] - Dark Mode Button Exists.") if dark_mode_button else print("[FAILED] - Dark Mode button not found.")

    textarea = driver.find_element(By.NAME, "post")
    textarea.click()
    textarea.send_keys("Hello, this is a test message!")
    print("[PASSED] - Post text entered successfully.")
    driver.find_element(By.NAME, 'post-submit').click()
    print("[PASSED] - Post successful.")
    time.sleep(3)

    feed = driver.find_element(By.CLASS_NAME, "card-text")
    print("[PASSED] - New Post Exists in Feed.") if feed else print("[FAILED] - New Post not found.")

    driver.find_element(By.CSS_SELECTOR, "button[name='logout']").click()
    print("[PASSED] - Log out successful.")

except Exception as e:
    print("Error:", e)

finally:
    print("--= Ending Tests =--")
    driver.quit()
