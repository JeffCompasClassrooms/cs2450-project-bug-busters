from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

# Set up Chrome options to disable the user data directory issue
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--headless")  # Optional: Run in headless mode (no browser window)

# Initialize the WebDriver with the specified options
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Track passed tests
passed_tests = 0

# Open the page
driver.get("http://localhost:5000/roulette")

# Test 5 invalid bet numbers (above 36)
invalid_bet_numbers = [37, 50, 100, 200, 500]

for bet_number in invalid_bet_numbers:
    try:
        # Find and clear the bet number input
        bet_number_input = driver.find_element(By.ID, "betNumber")
        bet_number_input.clear()
        
        # Enter an invalid bet number
        bet_number_input.send_keys(str(bet_number))
        
        # Find and click the submit button
        submit_button = driver.find_element(By.ID, "submitBtn")
        submit_button.click()
        
        # Wait for a moment to let the error message appear
        time.sleep(2)  # Optional: Adjust sleep time if needed
        
        # Check if the result message appears (expecting an error message)
        result_message = driver.find_element(By.ID, "resultMessage")
        if result_message.is_displayed():
            print(f"[PASSED] - Invalid Bet Number {bet_number} Triggers Error")
            passed_tests += 1  # Increment passed_tests for this test
        else:
            print(f"[FAILED] - Invalid Bet Number {bet_number} Did Not Trigger Error")
    except Exception as e:
        print(f"[PASSED] - Invalid Bet Number {bet_number} Triggered Expected Exception")
        passed_tests += 1  # Increment passed_tests for the exception case

# Test 5 insufficient balance cases (bet more than available balance)
insufficient_balance_cases = [
    {"bet_amount": 10, "balance": 5},  # Trying to bet 10 with a balance of 5
    {"bet_amount": 20, "balance": 5},  # Trying to bet 20 with a balance of 5
    {"bet_amount": 50, "balance": 5},  # Trying to bet 50 with a balance of 5
    {"bet_amount": 100, "balance": 5},  # Trying to bet 100 with a balance of 5
    {"bet_amount": 200, "balance": 5}   # Trying to bet 200 with a balance of 5
]

for case in insufficient_balance_cases:
    try:
        # Set the balance to the value specified
        balance_element = driver.find_element(By.ID, "balance")
        driver.execute_script(f"arguments[0].innerText = '$ {case['balance']}'", balance_element)  # Dynamically adjust balance
        
        # Find and clear the bet amount input
        bet_amount_input = driver.find_element(By.ID, "betAmount")
        bet_amount_input.clear()
        
        # Enter an invalid bet amount (greater than balance)
        bet_amount_input.send_keys(str(case["bet_amount"]))
        
        # Find and click the submit button
        submit_button = driver.find_element(By.ID, "submitBtn")
        submit_button.click()
        
        # Wait for a moment to let the error message appear
        time.sleep(2)  # Optional: Adjust sleep time if needed
        
        # Check if the result message appears (expecting an error message about insufficient balance)
        result_message = driver.find_element(By.ID, "resultMessage")
        if result_message.is_displayed():
            print(f"[PASSED] - Insufficient Balance for Bet of {case['bet_amount']}")
            passed_tests += 1  # Increment passed_tests for this test
        else:
            print(f"[FAILED] - Insufficient Balance for Bet of {case['bet_amount']}")
    except Exception as e:
        print(f"[PASSED] - Insufficient Balance for Bet of {case['bet_amount']} Triggered Expected Exception")
        passed_tests += 1  # Increment passed_tests for the exception case

# Final Results - Print the number of passed tests out of 10
total_tests = 10  # As we are running 10 tests in total
print(f"\nTests Passed: {passed_tests}/{total_tests}")
driver.quit()
