import os
import time
import unittest
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class FlightBookingBlazeDemo(unittest.TestCase):
    def setUp(self):
        load_dotenv(override=True)
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.wait = WebDriverWait(self.driver, 20)

    def test_flight_booking(self):
        driver = self.driver
        wait = self.wait

        base_url = os.getenv("BASE_URL4", "").strip()
        self.assertTrue(base_url, "BASE_URL4 is empty. Check .env")

        first_name = os.getenv("FIRST_NAME", "Test").strip()
        last_name = os.getenv("LAST_NAME", "User").strip()
        email = os.getenv("EMAIL", "test@example.com").strip()
        phone = os.getenv("PHONE", "77001234567").strip()

        # 1) Open site
        driver.get(base_url)

        # Title checkpoint
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        self.assertIn("BlazeDemo", driver.title)
        print("Checkpoint 1: Title checkpoint OK ->", driver.title)

        # 2) Choose departure and destination (CSS)
        from_select = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "select[name='fromPort']")))
        to_select = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "select[name='toPort']")))

        Select(from_select).select_by_visible_text("Boston")
        Select(to_select).select_by_visible_text("New York")
        print("Checkpoint 2: From/To selected")

        # 3) Click Find Flights (XPath)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Find Flights']"))).click()
        print("Checkpoint 3: Find Flights clicked")

        # 4) Pick first flight (XPath)
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@type='submit' and @value='Choose This Flight'])[1]"))).click()
        print("Checkpoint 4: First flight chosen")

        # 5) Fill passenger form (CSS + ID)
        wait.until(EC.presence_of_element_located((By.ID, "inputName"))).send_keys(f"{first_name} {last_name}")
        driver.find_element(By.ID, "address").send_keys("Almaty, Kazakhstan")
        driver.find_element(By.ID, "city").send_keys("Almaty")
        driver.find_element(By.ID, "state").send_keys("Almaty")
        driver.find_element(By.ID, "zipCode").send_keys("050000")

        # card fields (fake test data)
        Select(driver.find_element(By.ID, "cardType")).select_by_visible_text("Visa")
        driver.find_element(By.ID, "creditCardNumber").send_keys("4111111111111111")
        driver.find_element(By.ID, "creditCardMonth").clear()
        driver.find_element(By.ID, "creditCardMonth").send_keys("12")
        driver.find_element(By.ID, "creditCardYear").clear()
        driver.find_element(By.ID, "creditCardYear").send_keys("2030")
        driver.find_element(By.ID, "nameOnCard").send_keys(f"{first_name} {last_name}")

        print("Checkpoint 5: Passenger form filled")
        time.sleep(2)

        # Extra checkpoint: ensure we're on purchase page
        self.assertIn("purchase", driver.current_url.lower())
        print("Checkpoint 6: Reached purchase page (no payment done)")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()