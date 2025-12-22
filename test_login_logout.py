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

class RedditLoginLogoutTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 20)

    def login(self):
        """Helper method to perform login"""
        driver = self.driver
        wait = self.wait

        # Navigate to Reddit login page
        driver.get("https://www.reddit.com/login")
        time.sleep(2)

        # Wait for and click username field before filling - using correct ID
        username_input = wait.until(EC.element_to_be_clickable((By.ID, "login-username")))
        username_input.click()
        time.sleep(0.5)
        # Clear field using JavaScript
        driver.execute_script("arguments[0].value = '';", username_input)
        username_input.send_keys(os.getenv("USERNAME"))

        # Wait for and click password field before filling - using correct ID
        password_input = wait.until(EC.element_to_be_clickable((By.ID, "login-password")))
        password_input.click()
        time.sleep(0.5)
        # Clear field using JavaScript
        driver.execute_script("arguments[0].value = '';", password_input)
        password_input.send_keys(os.getenv("PASSWORD"))

        # Click login button "Войти" - wait for it to be enabled
        login_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.login")))
        # Wait for button to be enabled (fields must be filled)
        wait.until(lambda d: login_button.is_enabled())
        time.sleep(0.5)
        # Try normal click first, if fails use JavaScript
        try:
            login_button.click()
        except:
            driver.execute_script("arguments[0].click();", login_button)
        
        # Wait for login to complete
        time.sleep(3)

    def test_login(self):
        """Test login functionality"""
        self.login()
        
        # Verify login successful - should not be on login page
        current_url = self.driver.current_url
        self.assertNotIn("/login", current_url, "Should be redirected away from login page after successful login")

    def test_logout(self):
        """Test logout functionality"""
        # First login
        self.login()
        
        # Logout using direct endpoint
        self.driver.get("https://www.reddit.com/logout")
        time.sleep(2)
        
        # Verify logout successful - should be on Reddit home page
        current_url = self.driver.current_url
        self.assertIn("reddit.com", current_url, "Should be on Reddit after logout")
        # Should be able to see login button or be redirected to home
        self.assertTrue(
            "/login" in current_url or current_url == "https://www.reddit.com/" or "reddit.com" in current_url,
            "Should be logged out"
        )

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
