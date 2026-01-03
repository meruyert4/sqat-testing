from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        
        # Locators
        self.booking_checkbox_xpath = "//label[contains(., 'Booking.com')]"
        self.from_input_id = "avia_form_origin-input"
        self.to_input_id = "avia_form_destination-input"
        self.date_picker_button_xpath = '/html/body/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/form/div[1]/div[3]/div[1]/div[1]/button[1]'
        self.target_date_css = 'div.s__vY0Kp_7_YUAgIkqP:nth-child(3) > table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(5) > td:nth-child(3) > div:nth-child(1) > button:nth-child(1) > div:nth-child(2)'
        self.confirm_date_xpath = "//button[contains(., 'Выбрать')] | //button[contains(., 'Готово')] | /html/body/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/form/div[1]/div[3]/div[1]/div[2]/div[1]/div/div/div/div/button"
        self.search_btn_css = 'button[data-test-id="form-submit"]'

    def open(self):
        self.driver.get("https://www.aviasales.kz")
        
    def disable_booking_checkbox(self):
        print("Removing checkbox")
        try:
            booking_label = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, self.booking_checkbox_xpath)
            ))
            checkbox_input = booking_label.find_element(By.TAG_NAME, "input")
            
            if checkbox_input.is_selected():
                self.driver.execute_script("arguments[0].click();", booking_label)
                print("Booking.com checkbox was active - disabled it.")
            else:
                self.driver.execute_script("arguments[0].click();", booking_label)
                print("Clicked on Booking.com checkbox (inactive mode).")
        except Exception as e:
            print(f"Failed to handle Booking checkbox: {e}")
    
    def enter_departure_city(self, city):
        from_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{self.from_input_id}"]')))
        from_input.clear()
        from_input.send_keys(city)
    
    def enter_destination_city(self, city):
        to_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{self.to_input_id}"]')))
        to_input.clear()
        to_input.send_keys(city)
    
    def select_date(self):
        date_picker_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.date_picker_button_xpath)))
        date_picker_button.click()
        
        target_date = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.target_date_css)))
        target_date.click()
        print("Date selected: 28.02.2025")
    
    def confirm_date_selection(self):
        try:
            confirm_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.confirm_date_xpath)))
            confirm_btn.click()
            print("Confirm button clicked")
        except Exception as e:
            print("No new tab or confirm button issues, staying on current page.")
    
    def click_search_button(self):
        print("Looking for search button...")
        try:
            search_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.search_btn_css)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_button)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", search_button)
            print("Search button clicked via JS!")
        except Exception as e:
            print(f"Failed to click search button: {e}")
            print("Trying Plan B: Pressing ENTER in destination field...")
            to_input = self.driver.find_element(By.XPATH, f'//*[@id="{self.to_input_id}"]')
            to_input.send_keys(Keys.ENTER)
    
    def search_flights(self, from_city, to_city):
        print("Filling search form...")
        self.disable_booking_checkbox()
        self.enter_departure_city(from_city)
        self.enter_destination_city(to_city)
        self.select_date()
        self.confirm_date_selection()
        self.click_search_button()
