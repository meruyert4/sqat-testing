from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time


class BookingPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        
        # Locators
        self.email_input_id = "contact_email"
        self.phone_input_id = "contact_cellphone"
        self.name_input_id = "firstName_0"
        self.lastname_input_id = "lastName_0"
        self.gender_female_id = "gender_F_0"
        self.birth_day_id = "birthDateDay_0"
        self.birth_month_id = "birthDateMonth_0"
        self.birth_year_id = "birthDateYear_0"
        self.passport_input_id = "passportNoAll_0"
        self.passport_day_id = "passportDay_0"
        self.passport_month_id = "passportMonth_0"
        self.passport_year_id = "passportYear_0"
        self.nationality_dropdown_css = '.searchable-select__selection'
        self.nationality_search_css = '.searchable-select__search'
        self.comfort_package_xpath = "//div[contains(@class, 'provider-package__select') and .//p[text()='Comfort']]"
    
    def fill_email(self, email):
        email_input = self.wait.until(
            EC.presence_of_element_located((By.XPATH, f'//*[@id="{self.email_input_id}"]'))
        )
        email_input.clear()
        email_input.send_keys(email)
    
    def fill_phone(self, phone):
        phone_input = self.driver.find_element(By.XPATH, f'//*[@id="{self.phone_input_id}"]')
        phone_input.clear()
        phone_input.send_keys(phone)
    
    def fill_name(self, name):
        name_input = self.driver.find_element(By.XPATH, f'//*[@id="{self.name_input_id}"]')
        name_input.clear()
        name_input.send_keys(name)
    
    def fill_lastname(self, lastname):
        lastname_input = self.driver.find_element(By.XPATH, f'//*[@id="{self.lastname_input_id}"]')
        lastname_input.clear()
        lastname_input.send_keys(lastname)
    
    def select_gender_female(self):
        female_label = self.driver.find_element(By.XPATH, f'//*[@id="{self.gender_female_id}"]')
        if not female_label.is_selected():
            try:
                close_overlay = self.driver.find_elements(By.CSS_SELECTOR, '.membership-container [data-testid="closeIcon"]')
                if close_overlay:
                    close_overlay[0].click()
                    WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located((By.ID, 'membershipContainer')))
                female_label.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", female_label)
    
    def fill_date_of_birth(self, day, month, year):
        Select(self.driver.find_element(By.XPATH, f'//*[@id="{self.birth_day_id}"]')).select_by_value(f"{day:02d}")
        Select(self.driver.find_element(By.XPATH, f'//*[@id="{self.birth_month_id}"]')).select_by_value(f"{month:02d}")
        Select(self.driver.find_element(By.XPATH, f'//*[@id="{self.birth_year_id}"]')).select_by_value(str(year))
    
    def fill_passport_number(self, passport_number):
        passport_input = self.driver.find_element(By.XPATH, f'//*[@id="{self.passport_input_id}"]')
        passport_input.clear()
        passport_input.send_keys(passport_number)
    
    def fill_passport_expiration(self, day, month, year):
        Select(self.driver.find_element(By.XPATH, f'//*[@id="{self.passport_day_id}"]')).select_by_value(f"{day:02d}")
        Select(self.driver.find_element(By.XPATH, f'//*[@id="{self.passport_month_id}"]')).select_by_value(f"{month:02d}")
        Select(self.driver.find_element(By.XPATH, f'//*[@id="{self.passport_year_id}"]')).select_by_value(str(year))
    
    def select_nationality(self, nationality):
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.nationality_dropdown_css))
        )
        dropdown.click()
        
        search_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, self.nationality_search_css))
        )
        search_input.clear()
        search_input.send_keys(nationality)
        
        option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'searchable-select__option') and text()='{nationality}']"))
        )
        option.click()
        print(f"Selected nationality: {nationality}")
    
    def select_comfort_package(self):
        comfort_package = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.comfort_package_xpath))
        )
        comfort_package.click()
        print("Selected 'Comfort' flight package")
    
    def fill_booking_form(self, email, phone, name, lastname, birth_day, birth_month, 
                         birth_year, passport_number, passport_exp_day, passport_exp_month, 
                         passport_exp_year, nationality):
        self.fill_email(email)
        self.fill_phone(phone)
        self.fill_name(name)
        self.fill_lastname(lastname)
        self.select_gender_female()
        self.fill_date_of_birth(birth_day, birth_month, birth_year)
        self.fill_passport_number(passport_number)
        self.fill_passport_expiration(passport_exp_day, passport_exp_month, passport_exp_year)
        self.select_nationality(nationality)
        self.select_comfort_package()
        time.sleep(7)
        print("finished")
