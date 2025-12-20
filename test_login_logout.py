# Create a test case for login and logout functionality (30pts)

import unittest
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

load_dotenv()


class LoginLogoutTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install())
        )
        self.driver.maximize_window()

    def test_login(self):
        """Test login functionality"""
        driver = self.driver
        
        # Go to the login page
        driver.get(os.getenv("BASE_URL3"))
        time.sleep(1)

        # Enter username
        username_input = driver.find_element(By.ID, "username")
        username_input.send_keys(os.getenv("USERNAME"))

        # Enter password
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys(os.getenv("PASSWORD"))

        # Click login button
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        time.sleep(1)

        # Verify login successful
        flash_message = driver.find_element(By.ID, "flash")
        self.assertIn("You logged into a secure area!", flash_message.text)

    def test_logout(self):
        """Test logout functionality"""
        driver = self.driver
        
        # First login
        driver.get(os.getenv("BASE_URL3"))
        time.sleep(1)

        driver.find_element(By.ID, "username").send_keys(os.getenv("USERNAME"))
        driver.find_element(By.ID, "password").send_keys(os.getenv("PASSWORD"))
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1)

        # Now logout
        logout_button = driver.find_element(By.CSS_SELECTOR, "a[href='/logout']")
        logout_button.click()
        time.sleep(1)

        # Verify logout successful
        flash_message = driver.find_element(By.ID, "flash")
        self.assertIn("You logged out of the secure area!", flash_message.text)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()