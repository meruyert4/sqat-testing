import unittest
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

load_dotenv()

class SearchTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install())
        )

    def test_search_github(self):
        driver = self.driver
        driver.get(os.getenv("BASE_URL1"))

        search_button = driver.find_element(By.CSS_SELECTOR, "button[data-target='qbsearch-input.inputButton']")
        search_button.click()

        time.sleep(1)

        search_input = driver.find_element(By.CSS_SELECTOR, "input#query-builder-test")
        search_input.send_keys("Selenium")
        search_input.submit()

        time.sleep(2)

        self.assertIn("Selenium", driver.page_source)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
