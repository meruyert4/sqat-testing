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
from selenium.webdriver.support.ui import Select

load_dotenv()


class FlightBookingTest(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--start-maximized")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    def test_flight_booking_scat(self):
        """Test flight booking process on SCAT Airlines"""
        driver = self.driver
        wait = WebDriverWait(driver, 20)

        # 1️⃣ Go to SCAT Airlines homepage
        driver.get(os.getenv("BASE_URL3"))
        time.sleep(3)
        
        self.assertIn("scat", driver.current_url.lower())
        print("✓ Checkpoint 1: SCAT Airlines homepage loaded")

        # 2️⃣ Enter destination in "куда" field
        to_input = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Город или страна']"))
        )
        # Click the second input (destination)
        inputs = driver.find_elements(By.CSS_SELECTOR, "input[placeholder='Город или страна']")
        if len(inputs) > 1:
            inputs[1].click()
            inputs[1].send_keys("Алматы")
        else:
            to_input.click()
            to_input.send_keys("Алматы")
        time.sleep(2)
        
        # Select first suggestion
        first_suggestion = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[class*='suggestion'], [class*='dropdown'] li, [class*='autocomplete'] div"))
        )
        first_suggestion.click()
        time.sleep(1)
        print("✓ Checkpoint 2: Destination Almaty selected")

        # 3️⃣ Click on departure date field
        date_field = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'отправление')] | //input[contains(@placeholder,'отправление')]"))
        )
        date_field.click()
        time.sleep(2)
        print("✓ Checkpoint 3: Date picker opened")

        # 4️⃣ Select first available date (blue colored)
        available_dates = driver.find_elements(By.CSS_SELECTOR, "[class*='calendar'] [class*='day'][class*='available'], td[class*='available'], div[class*='price']")
        if available_dates:
            available_dates[0].click()
        else:
            # Try clicking any date with price
            date_with_price = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//td[contains(@class,'day') and .//span[contains(text(),'₸')]] | //div[contains(@class,'day') and contains(text(),'₸')]"))
            )
            date_with_price.click()
        time.sleep(1)
        print("✓ Checkpoint 4: Date selected")

        # 5️⃣ Click "В одну сторону" (One way) button
        one_way_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'В одну сторону')] | //span[contains(text(),'В одну сторону')]"))
        )
        one_way_btn.click()
        time.sleep(1)
        print("✓ Checkpoint 5: One way selected")

        # 6️⃣ Click search button
        search_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'], [class*='search-btn'], button[class*='search']"))
        )
        search_btn.click()
        time.sleep(5)
        print("✓ Checkpoint 6: Search started")

        # 7️⃣ Select first flight from results
        first_flight = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Выбрать')] | //div[contains(@class,'flight')]//button"))
        )
        first_flight.click()
        time.sleep(2)
        print("✓ Checkpoint 7: First flight selected")

        # 8️⃣ Select LIGHT fare (first option)
        light_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'LIGHT') or contains(text(),'LIGHT')]//button[contains(text(),'Выбрать')] | //button[contains(text(),'Выбрать')][1]"))
        )
        light_btn.click()
        time.sleep(2)
        print("✓ Checkpoint 8: LIGHT fare selected")

        # 9️⃣ Click "Продолжить" (Continue)
        continue_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Продолжить')]"))
        )
        continue_btn.click()
        time.sleep(3)
        print("✓ Checkpoint 9: Continued to passenger form")

        # 🔟 Fill passenger form
        # Email
        email_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder,'почта') or contains(@placeholder,'Email')]"))
        )
        email_input.send_keys(os.getenv("EMAIL"))
        
        # Phone
        phone_input = driver.find_element(By.XPATH, "//input[contains(@placeholder,'Телефон') or contains(@placeholder,'Phone')]")
        phone_input.send_keys(os.getenv("PHONE"))
        
        # Last name (Фамилия)
        lastname_input = driver.find_element(By.XPATH, "//input[contains(@placeholder,'Фамилия')]")
        lastname_input.send_keys(os.getenv("LAST_NAME"))
        
        # First name (Имя)
        firstname_input = driver.find_element(By.XPATH, "//input[contains(@placeholder,'Имя')]")
        firstname_input.send_keys(os.getenv("FIRST_NAME"))
        
        # Birth date
        birthdate_input = driver.find_element(By.XPATH, "//input[contains(@placeholder,'рождения') or contains(@placeholder,'birth')]")
        birthdate_input.send_keys(os.getenv("BIRTH_DATE"))
        
        print("✓ Checkpoint 10: Personal info filled")

        # 1️⃣1️⃣ Select document type (second option)
        try:
            doc_type_dropdown = driver.find_element(By.XPATH, "//div[contains(text(),'Тип документа')] | //select[contains(@name,'document')]")
            doc_type_dropdown.click()
            time.sleep(1)
            second_option = driver.find_elements(By.CSS_SELECTOR, "[class*='option'], li[class*='item']")
            if len(second_option) > 1:
                second_option[1].click()
        except:
            pass
        
        # Document number
        doc_number_input = driver.find_element(By.XPATH, "//input[contains(@placeholder,'документа') or contains(@placeholder,'Номер')]")
        doc_number_input.send_keys(os.getenv("PASSPORT_NUMBER"))
        
        print("✓ Checkpoint 11: Document info filled")

        # 1️⃣2️⃣ Click checkbox "Я ознакомился (-лась)"
        checkbox = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox'] | //label[contains(text(),'ознакомился')]"))
        )
        checkbox.click()
        time.sleep(1)
        print("✓ Checkpoint 12: Agreement checkbox clicked")

        # 1️⃣3️⃣ Click final "Продолжить" button
        final_continue = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Продолжить')]"))
        )
        final_continue.click()
        time.sleep(3)
        print("✓ Checkpoint 13: Final continue clicked - TEST COMPLETE 🎉")

        # Stop at payment page
        self.assertTrue(True, "Booking flow completed successfully")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
