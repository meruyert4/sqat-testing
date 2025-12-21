import unittest
import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()


class FlightBookingTest(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    def test_flight_booking_scat(self):
        driver = self.driver
        wait = WebDriverWait(driver, 30)

        # 1. Go to SCAT Airlines
        driver.get(os.getenv("BASE_URL3"))
        time.sleep(5)
        self.assertIn("scat", driver.current_url.lower())
        
        # Wait for page to be fully loaded
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        time.sleep(2)  # Additional wait for dynamic content
        
        # Wait for search form to be present
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "//form | //input[@type='text'] | //div[contains(@class,'search')]")))
        except:
            pass  # Continue even if form selector doesn't match exactly
        
        print("Checkpoint 1: Homepage loaded")

        # 2. Enter from Astana - try multiple selector strategies
        from_input = None
        selectors = [
            "//input[contains(@placeholder,'From')]",
            "//input[contains(@placeholder,'from')]",
            "//input[contains(@placeholder,'FROM')]",
            "//label[contains(text(),'from') or contains(text(),'From')]/following-sibling::input",
            "//label[contains(text(),'from') or contains(text(),'From')]/../input",
            "(//form//input[@type='text'])[1]",
            "(//div[contains(@class,'search')]//input)[1]",
            "(//input[@type='text'])[1]"
        ]
        
        for selector in selectors:
            try:
                from_input = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                print(f"Found 'from' input using selector: {selector}")
                break
            except:
                continue
        
        if not from_input:
            raise Exception("Could not find 'from' input field")
        
        from_input.click()
        time.sleep(1)
        from_input.clear()
        from_input.send_keys("Astana")
        time.sleep(2)

        # 3. Enter destination Almaty - try multiple selector strategies
        to_input = None
        selectors = [
            "//input[contains(@placeholder,'To') and not(contains(@placeholder,'From'))]",
            "//input[contains(@placeholder,'to') and not(contains(@placeholder,'from'))]",
            "//input[contains(@placeholder,'TO') and not(contains(@placeholder,'FROM'))]",
            "//label[contains(text(),'to') or contains(text(),'To')]/following-sibling::input[not(contains(@placeholder,'from'))]",
            "//label[contains(text(),'to') or contains(text(),'To')]/../input[not(contains(@placeholder,'from'))]",
            "(//form//input[@type='text'])[2]",
            "(//div[contains(@class,'search')]//input)[2]",
            "(//input[@type='text'])[2]"
        ]
        
        for selector in selectors:
            try:
                to_input = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                print(f"Found 'to' input using selector: {selector}")
                break
            except:
                continue
        
        if not to_input:
            raise Exception("Could not find 'to' input field")
        
        to_input.click()
        time.sleep(1)
        to_input.clear()
        to_input.send_keys("Almaty")
        time.sleep(2)
        
        first_suggestion = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//ul//li | //div[contains(@class,'dropdown')]//div"))
        )
        first_suggestion.click()
        print("Checkpoint 2: Destination selected")

        # 3. Select date
        date_field = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'date')]"))
        )
        date_field.click()
        time.sleep(2)
        
        available_date = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//td[contains(@class,'available')]"))
        )
        available_date.click()
        print("Checkpoint 3: Date selected")

        # 4. Click One way
        one_way_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'One way')]"))
        )
        one_way_btn.click()
        print("Checkpoint 4: One way selected")

        # 5. Search
        search_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        search_btn.click()
        time.sleep(5)
        print("Checkpoint 5: Search done")

        # 6. Select first flight
        first_flight = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Select')]"))
        )
        first_flight.click()
        time.sleep(3)
        print("Checkpoint 6: Flight selected")

        # 7. Select first bundle (OPTIMUM or FLEX - whichever is first)
        time.sleep(2)  # Wait for bundle selection page to load
        first_bundle_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//button[contains(text(),'Select')])[1]"))
        )
        first_bundle_btn.click()
        time.sleep(3)  # Wait a bit after selecting bundle
        print("Checkpoint 7: First bundle selected")

        # 8. Continue to form
        continue_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Continue')]"))
        )
        continue_btn.click()
        time.sleep(3)
        print("Checkpoint 8: Passenger form opened")

        # 9. Fill form - Contact section first
        email_input = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[contains(@placeholder,'mail') or contains(@placeholder,'Email')]"))
        )
        email_input.clear()
        email_input.send_keys(os.getenv("EMAIL"))
        time.sleep(1)
        
        phone_input = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[contains(@placeholder,'Phone')]"))
        )
        phone_input.clear()
        phone_input.send_keys(os.getenv("PHONE"))
        time.sleep(1)
        
        # Fill passenger details
        lastname_input = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[contains(@placeholder,'Last') or contains(@placeholder,'last')]"))
        )
        lastname_input.clear()
        lastname_input.send_keys(os.getenv("LAST_NAME"))
        time.sleep(1)
        
        firstname_input = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[contains(@placeholder,'First') or contains(@placeholder,'first')]"))
        )
        firstname_input.clear()
        firstname_input.send_keys(os.getenv("FIRST_NAME"))
        time.sleep(1)
        
        birthdate_input = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[contains(@placeholder,'birth') or contains(@placeholder,'Birth')]"))
        )
        birthdate_input.clear()
        birthdate_input.send_keys(os.getenv("BIRTH_DATE"))
        time.sleep(1)
        
        # Select gender - female icon (second one)
        # Find buttons near the birth date field and select the second one
        gender_icon = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//input[contains(@placeholder,'birth') or contains(@placeholder,'Birth')]/ancestor::div[1]//button)[2] | (//input[contains(@placeholder,'birth') or contains(@placeholder,'Birth')]/following-sibling::*//button)[2] | (//div[contains(text(),'Adult')]/ancestor::div[1]//button)[2]"))
        )
        gender_icon.click()
        time.sleep(1)
        
        doc_input = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[contains(@placeholder,'document') or contains(@placeholder,'Document')]"))
        )
        doc_input.clear()
        doc_input.send_keys(os.getenv("PASSPORT_NUMBER"))
        time.sleep(1)
        print("Checkpoint 9: Form filled")

        # 10. Click checkbox and continue
        checkbox = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox']"))
        )
        if not checkbox.is_selected():
            checkbox.click()
        time.sleep(1)
        
        final_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Continue')]"))
        )
        final_btn.click()
        time.sleep(2)
        print("Checkpoint 10: TEST COMPLETE")

        self.assertTrue(True)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
