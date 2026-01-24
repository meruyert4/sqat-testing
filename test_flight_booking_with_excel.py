import unittest
import time
import os
import argparse
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from excel_reader import read_test_data
from test_config import validate_browser_os_combination, get_os_config

load_dotenv()

def parse_command_line_args():
    """Parse command line arguments for test configuration"""
    parser = argparse.ArgumentParser(description='Run Aviasales flight booking test on BrowserStack')
    parser.add_argument(
        '--browser',
        type=str,
        default='chrome',
        choices=['chrome', 'firefox', 'safari'],
        help='Browser to use (chrome, firefox, safari)'
    )
    parser.add_argument(
        '--os',
        type=str,
        default='windows',
        choices=['windows', 'macos'],
        help='Operating system (windows or macos). Windows supports: chrome, firefox. macOS supports: chrome, firefox, safari'
    )
    parser.add_argument(
        '--excel',
        type=str,
        default='test_data.xlsx',
        help='Path to Excel file with test data'
    )
    parser.add_argument(
        '--local',
        action='store_true',
        default=False,
        help='Run tests locally instead of BrowserStack (default: False, runs on BrowserStack)'
    )
    args, unknown = parser.parse_known_args()
    return args, unknown

class AviasalesFlightBookingTest(unittest.TestCase):
    USE_BROWSERSTACK = True
    BROWSER = 'chrome'
    OS_TYPE = 'windows'
    EXCEL_FILE_PATH = 'test_data.xlsx'
    
    def setUp(self):
        self.test_data = read_test_data(self.EXCEL_FILE_PATH)
        print(f"\n[INFO] Starting browser: {self.BROWSER}")
        self.driver = self.setup_browserstack_driver() if self.USE_BROWSERSTACK else self.setup_local_driver()
        print("[INFO] Browser opened successfully")
        self.driver.maximize_window()
        print("[INFO] Window maximized")
    
    def setup_local_driver(self):
        if self.BROWSER.lower() == "chrome":
            return webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        elif self.BROWSER.lower() == "firefox":
            return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        raise ValueError(f"Unsupported browser: {self.BROWSER}")
    
    def setup_browserstack_driver(self):
        username = os.getenv('BROWSERSTACK_USERNAME')
        access_key = os.getenv('BROWSERSTACK_ACCESS_KEY')
        if not username or not access_key:
            raise ValueError("BrowserStack credentials missing in .env")
        
        browser_lower = self.BROWSER.lower()
        if browser_lower == "chrome":
            options = ChromeOptions()
        elif browser_lower == "firefox":
            options = FirefoxOptions()
        elif browser_lower == "safari":
            options = SafariOptions()
        else:
            raise ValueError(f"Unsupported browser: {self.BROWSER}")
        
        os_config = get_os_config(self.OS_TYPE)
        
        options.set_capability('browserVersion', 'latest')
        options.set_capability('bstack:options', {
            'os': os_config['os'],
            'osVersion': os_config['osVersion'],
            'projectName': 'Aviasales Automation',
            'buildName': 'Flight Booking Test',
            'sessionName': f'{self.OS_TYPE.upper()} - {self.BROWSER.upper()}'
        })
        
        hub_url = f"https://{username}:{access_key}@hub-cloud.browserstack.com/wd/hub"
        return webdriver.Remote(command_executor=hub_url, options=options)
    
    def test_flight_booking_process(self):
        driver = self.driver
        wait = WebDriverWait(driver, 20)
        
        print(f"[INFO] Opening URL: {self.test_data['url']}")
        driver.get(self.test_data['url'])
        time.sleep(5)
        
        self.handle_booking_checkbox(wait)
        self.fill_search_form(wait)
        self.search_flights(wait)
        self.select_flight(wait)
        self.fill_passenger_details(wait)
        self.select_comfort_package(wait)
        time.sleep(3)
    
    def handle_booking_checkbox(self, wait):
        try:
            booking_label = wait.until(EC.presence_of_element_located((By.XPATH, "//label[contains(., 'Booking.com')]")))
            self.driver.execute_script("arguments[0].click();", booking_label)
        except:
            pass
    
    def fill_search_form(self, wait):
        from_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="avia_form_origin-input"]')))
        from_input.clear()
        from_input.send_keys(self.test_data['from_city'])
        
        to_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="avia_form_destination-input"]')))
        to_input.clear()
        to_input.send_keys(self.test_data['to_city'])
        
        date_picker = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/form/div[1]/div[3]/div[1]/div[1]/button[1]')))
        date_picker.click()
        
        target_date = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.s__vY0Kp_7_YUAgIkqP:nth-child(3) > table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(5) > td:nth-child(3) > div:nth-child(1) > button:nth-child(1) > div:nth-child(2)')))
        target_date.click()
        
        try:
            confirm_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Выбрать')] | //button[contains(., 'Готово')]")))
            confirm_btn.click()
        except:
            pass
    
    def search_flights(self, wait):
        driver = self.driver
        initial_url = driver.current_url
        
        search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test-id="form-submit"]')))
        driver.execute_script("arguments[0].click();", search_button)
        
        try:
            WebDriverWait(driver, 20).until(lambda d: "/search" in d.current_url or d.current_url != initial_url)
        except:
            driver.find_element(By.XPATH, '//*[@id="avia_form_destination-input"]').send_keys(Keys.ENTER)
        
        time.sleep(5)
        WebDriverWait(driver, 45).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-test-id="price"]')))
    
    def select_flight(self, wait):
        driver = self.driver
        
        ticket_price = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-test-id="price"]')))
        driver.execute_script("arguments[0].click();", ticket_price)
        
        buy_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/div/div[2]/div/div[2]/div[3]/div[1]/div[1]/div/div[2]/button')))
        original_window = driver.current_window_handle
        buy_button.click()
        
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        for window in driver.window_handles:
            if window != original_window:
                driver.switch_to.window(window)
                break
        time.sleep(2)
    
    def fill_passenger_details(self, wait):
        driver = self.driver
        d = self.test_data
        
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="contact_email"]'))).send_keys(d['email'])
        driver.find_element(By.XPATH, '//*[@id="contact_cellphone"]').send_keys(d['phone'])
        driver.find_element(By.XPATH, '//*[@id="firstName_0"]').send_keys(d['name'])
        driver.find_element(By.XPATH, '//*[@id="lastName_0"]').send_keys(d['lastname'])
        
        try:
            driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, '//*[@id="gender_F_0"]'))
        except:
            pass
        
        Select(driver.find_element(By.XPATH, '//*[@id="birthDateDay_0"]')).select_by_value(f"{int(d['birth_day']):02d}")
        Select(driver.find_element(By.XPATH, '//*[@id="birthDateMonth_0"]')).select_by_value(f"{int(d['birth_month']):02d}")
        Select(driver.find_element(By.XPATH, '//*[@id="birthDateYear_0"]')).select_by_value(str(d['birth_year']))
        
        driver.find_element(By.XPATH, '//*[@id="passportNoAll_0"]').send_keys(d['passport_number'])
        
        Select(driver.find_element(By.XPATH, '//*[@id="passportDay_0"]')).select_by_value(f"{int(d['passport_exp_day']):02d}")
        Select(driver.find_element(By.XPATH, '//*[@id="passportMonth_0"]')).select_by_value(f"{int(d['passport_exp_month']):02d}")
        Select(driver.find_element(By.XPATH, '//*[@id="passportYear_0"]')).select_by_value(str(d['passport_exp_year']))
        
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.searchable-select__selection'))).click()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.searchable-select__search'))).send_keys(d['nationality'])
        wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'searchable-select__option') and text()='{d['nationality']}']"))).click()
    
    def select_comfort_package(self, wait):
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'provider-package__select') and .//p[text()='Comfort']]"))).click()
    
    def tearDown(self):
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    import sys
    
    args, unknown = parse_command_line_args()
    
    AviasalesFlightBookingTest.USE_BROWSERSTACK = not args.local
    AviasalesFlightBookingTest.BROWSER = args.browser
    AviasalesFlightBookingTest.OS_TYPE = args.os
    AviasalesFlightBookingTest.EXCEL_FILE_PATH = args.excel
    
    validate_browser_os_combination(args.browser, args.os)
    
    print(f"\n[CONFIG] BrowserStack: {AviasalesFlightBookingTest.USE_BROWSERSTACK}")
    print(f"[CONFIG] Browser: {args.browser.upper()}")
    print(f"[CONFIG] OS: {args.os.upper()}")
    print(f"[CONFIG] Excel: {args.excel}\n")
    
    sys.argv = [sys.argv[0]] + unknown
    unittest.main()
