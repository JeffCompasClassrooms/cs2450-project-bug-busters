from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

chrome_driver_path = "/usr/local/bin/chromedriver" 
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

try:
    driver.get("http://localhost:5000/loginscreen")
    time.sleep(2)

    print("--= Beginning Tests =--")

    login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Login']")
    print("[PASSED] - Login Button Exists.")

    driver.find_element(By.NAME, "username").send_keys("osuna")
    driver.find_element(By.NAME, "password").send_keys("123")
    print("[PASSED] - Log in successful.")
    time.sleep(2)

    create_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Create']") 
    print("[PASSED] - Create Button Exists.")
    time.sleep(2)

    login_button.click()
    time.sleep(2)

    textarea = driver.find_element(By.CSS_SELECTOR, "textarea[class='form-control'][name='post']")
    textarea.send_keys("Hello, this is a test message!")
    print("[PASSED] - Post text entered successfully.")

    driver.find_element(By.CSS_SELECTOR, "button[name='logout']")
    print("[PASSED] - Log out successful.")

    driver.find_element(By.CSS_SELECTOR, "input[type='text'][name='name']").send_keys("paco")
    time.sleep(3)
    print("[PASSED] - Add friend button successful.")

    add_friend_button = driver.find_element(By.NAME, "addfriend")
    add_friend_button.click()
    
    driver.find_element(By.XPATH, '//a[@href="/friend/paco"]')
    print("[PASSED] - Friend Exists.")

    driver.find_element(By.XPATH, '//h1')
    print("[PASSED] - Title found.")
    time.sleep(3)

    post_button = driver.find_element(By.NAME, 'post-submit')
    print("[PASSED] - New Post Submitted")
    post_button.click()
    time.sleep(2)

    driver.find_element(By.CLASS_NAME, "card-text")
    print("[PASSED] - New Post Exists in Feed.")


except Exception as e:
    print("Error:", e)

finally:
    print("--= Ending Tests =--")
    driver.quit()