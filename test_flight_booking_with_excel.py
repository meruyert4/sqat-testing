import unittest
import time
import os
import argparse
import logging
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

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

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
        default=None,
        choices=['windows', 'macos'],
        help='Operating system (windows or macos). If not specified, auto-detected for local runs, defaults to windows for BrowserStack'
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
    
    # Auto-detect OS for local runs (ignore --os flag when --local is used)
    if args.local:
        import platform
        system = platform.system()
        if system == 'Darwin':
            args.os = 'macos'
        elif system == 'Windows':
            args.os = 'windows'
        else:
            args.os = 'windows'  # Default fallback
        logging.info(f"Local execution: Auto-detected OS as {args.os}")
    elif args.os is None:
        args.os = 'windows'  # Default for BrowserStack
    
    return args, unknown

class AviasalesFlightBookingTest(unittest.TestCase):
    USE_BROWSERSTACK = True
    BROWSER = 'chrome'
    OS_TYPE = 'windows'
    EXCEL_FILE_PATH = 'test_data.xlsx'
    
    def setUp(self):
        self.test_data = read_test_data(self.EXCEL_FILE_PATH)
        logging.info(f"Starting browser: {self.BROWSER}")
        try:
            self.driver = self.setup_browserstack_driver() if self.USE_BROWSERSTACK else self.setup_local_driver()
            logging.info("Browser opened successfully")
            self.driver.maximize_window()
            logging.info("Window maximized")
        except Exception as e:
            logging.error(f"Failed to setup browser: {str(e)}")
            raise
    
    def setup_local_driver(self):
        logging.info(f"Setting up local {self.BROWSER} driver")
        try:
            if self.BROWSER.lower() == "chrome":
                return webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            elif self.BROWSER.lower() == "firefox":
                return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
            elif self.BROWSER.lower() == "safari":
                return webdriver.Safari()
            raise ValueError(f"Unsupported browser: {self.BROWSER}")
        except Exception as e:
            logging.error(f"Failed to setup local driver: {str(e)}")
            raise
    
    def setup_browserstack_driver(self):
        logging.info(f"Setting up BrowserStack driver: {self.BROWSER} on {self.OS_TYPE}")
        username = os.getenv('BROWSERSTACK_USERNAME')
        access_key = os.getenv('BROWSERSTACK_ACCESS_KEY')
        if not username or not access_key:
            logging.error("BrowserStack credentials missing in .env")
            raise ValueError("BrowserStack credentials missing in .env")
        
        try:
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
            logging.info("Connecting to BrowserStack...")
            return webdriver.Remote(command_executor=hub_url, options=options)
        except Exception as e:
            logging.error(f"Failed to setup BrowserStack driver: {str(e)}")
            raise
    
    def test_flight_booking_process(self):
        driver = self.driver
        wait = WebDriverWait(driver, 30)  # Longer default wait for Safari
        
        try:
            logging.info(f"[STEP 1] Opening URL: {self.test_data['url']}")
            driver.get(self.test_data['url'])
            time.sleep(5)
            logging.info("Page loaded successfully")
            
            logging.info("[STEP 2] Handling booking checkbox")
            self.handle_booking_checkbox(wait)
            
            logging.info("[STEP 3] Filling search form")
            self.fill_search_form(wait)
            
            logging.info("[STEP 4] Searching for flights")
            self.search_flights(wait)
            
            logging.info("[STEP 5] Selecting flight")
            self.select_flight(wait)
            
            logging.info("[STEP 6] Filling passenger details")
            self.fill_passenger_details(wait)
            
            logging.info("[STEP 7] Selecting comfort package")
            self.select_comfort_package(wait)
            
            time.sleep(3)
            logging.info("Test completed successfully")
        except Exception as e:
            logging.error(f"Test failed: {str(e)}")
            raise
    
    def handle_booking_checkbox(self, wait):
        try:
            booking_label = wait.until(EC.presence_of_element_located((By.XPATH, "//label[contains(., 'Booking.com')]")))
            self.driver.execute_script("arguments[0].click();", booking_label)
            logging.info("Booking.com checkbox handled")
        except Exception as e:
            logging.warning(f"Booking checkbox not found or not clickable: {str(e)}")
    
    def fill_search_form(self, wait):
        try:
            from_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="avia_form_origin-input"]')))
            from_input.clear()
            from_input.send_keys(self.test_data['from_city'])
            logging.info(f"From city entered: {self.test_data['from_city']}")
            
            to_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="avia_form_destination-input"]')))
            to_input.clear()
            to_input.send_keys(self.test_data['to_city'])
            logging.info(f"To city entered: {self.test_data['to_city']}")
            
            date_picker = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/form/div[1]/div[3]/div[1]/div[1]/button[1]')))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", date_picker)
            time.sleep(0.5)
            date_picker.click()
            logging.info("Date picker opened")
            
            time.sleep(2)
            
            # Try multiple selectors for date selection (more flexible for Safari)
            date_selected = False
            selectors = [
                'div.s__vY0Kp_7_YUAgIkqP:nth-child(3) > table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(5) > td:nth-child(3) > div:nth-child(1) > button:nth-child(1) > div:nth-child(2)',
                'div[class*="calendar"] table tbody tr:nth-child(5) td:nth-child(3) button',
                'button[aria-label*="29"]',
                'table tbody tr td button div'
            ]
            
            for selector in selectors:
                try:
                    if 'div' == selector.split()[-1]:
                        # Find all date buttons and click a valid future date
                        date_buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        for btn in date_buttons:
                            if btn.is_displayed() and btn.is_enabled():
                                try:
                                    self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                                    time.sleep(0.3)
                                    self.driver.execute_script("arguments[0].click();", btn)
                                    date_selected = True
                                    logging.info("Date selected using JavaScript click")
                                    break
                                except:
                                    continue
                    else:
                        target_date = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", target_date)
                        time.sleep(0.3)
                        self.driver.execute_script("arguments[0].click();", target_date)
                        date_selected = True
                        logging.info(f"Date selected using selector: {selector}")
                    
                    if date_selected:
                        break
                except Exception as e:
                    logging.warning(f"Selector {selector} failed: {str(e)}")
                    continue
            
            if not date_selected:
                raise Exception("Could not select date with any selector")
            
            time.sleep(1)
            
            try:
                confirm_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Выбрать')] | //button[contains(., 'Готово')]")))
                self.driver.execute_script("arguments[0].click();", confirm_btn)
                logging.info("Date confirmed")
            except Exception as e:
                logging.warning(f"Date confirmation button not found: {str(e)}")
        except Exception as e:
            logging.error(f"Failed to fill search form: {str(e)}")
            raise
    
    def search_flights(self, wait):
        driver = self.driver
        initial_url = driver.current_url
        logging.info(f"Current URL: {initial_url}")
        
        try:
            search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test-id="form-submit"]')))
            driver.execute_script("arguments[0].click();", search_button)
            logging.info("Search button clicked")
            
            try:
                # Longer wait for Safari
                WebDriverWait(driver, 30).until(lambda d: "/search" in d.current_url or d.current_url != initial_url)
                logging.info(f"Navigated to: {driver.current_url}")
            except Exception as e:
                logging.warning(f"URL didn't change, trying alternate method: {str(e)}")
                driver.find_element(By.XPATH, '//*[@id="avia_form_destination-input"]').send_keys(Keys.ENTER)
            
            time.sleep(5)
            logging.info("Waiting for flight results to load...")
            # Longer wait for Safari
            WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-test-id="price"]')))
            logging.info("Flight results loaded")
        except Exception as e:
            logging.error(f"Failed to search flights: {str(e)}")
            logging.error(f"Final URL: {driver.current_url}")
            raise
    
    def select_flight(self, wait):
        driver = self.driver
        
        try:
            ticket_price = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-test-id="price"]')))
            driver.execute_script("arguments[0].click();", ticket_price)
            logging.info("Flight ticket clicked")
            
            # Wait longer for modal/popup to appear
            time.sleep(3)
            
            # Try multiple selectors for buy button with longer wait
            buy_button = None
            selectors = [
                (By.XPATH, '/html/body/div[2]/div/div/div/div/div[2]/div/div[2]/div[3]/div[1]/div[1]/div/div[2]/button'),
                (By.CSS_SELECTOR, 'button[data-test-id="flight-buy-button"]'),
                (By.XPATH, "//button[contains(text(), 'Купить') or contains(text(), 'Buy')]"),
                (By.CSS_SELECTOR, 'div[class*="buy"] button'),
                (By.XPATH, "//div[contains(@class, 'Button')]//button")
            ]
            
            for selector_type, selector in selectors:
                try:
                    buy_button = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((selector_type, selector))
                    )
                    logging.info(f"Buy button found with selector: {selector}")
                    break
                except Exception as e:
                    logging.warning(f"Selector failed: {selector}")
                    continue
            
            if not buy_button:
                raise Exception("Could not find buy button with any selector")
            
            original_window = driver.current_window_handle
            buy_button.click()
            logging.info("Buy button clicked")
            
            # Safari needs more time for window to open
            time.sleep(3)
            
            # Wait for new window with longer timeout
            WebDriverWait(driver, 30).until(EC.number_of_windows_to_be(2))
            for window in driver.window_handles:
                if window != original_window:
                    driver.switch_to.window(window)
                    logging.info("Switched to booking window")
                    break
            
            time.sleep(2)
            
            # Set page zoom to 80% for better element visibility in Safari
            driver.execute_script("document.body.style.zoom='80%'")
            logging.info("Page zoom set to 80%")
            time.sleep(1)
        except Exception as e:
            logging.error(f"Failed to select flight: {str(e)}")
            raise
    
    def fill_passenger_details(self, wait):
        driver = self.driver
        d = self.test_data
        
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="contact_email"]'))).send_keys(d['email'])
            logging.info("Email entered")
            
            driver.find_element(By.XPATH, '//*[@id="contact_cellphone"]').send_keys(d['phone'])
            logging.info("Phone entered")
            
            driver.find_element(By.XPATH, '//*[@id="firstName_0"]').send_keys(d['name'])
            logging.info("First name entered")
            
            driver.find_element(By.XPATH, '//*[@id="lastName_0"]').send_keys(d['lastname'])
            logging.info("Last name entered")
            
            try:
                driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, '//*[@id="gender_F_0"]'))
                logging.info("Gender selected")
            except Exception as e:
                logging.warning(f"Gender selection failed: {str(e)}")
            
            # Scroll and select birth date dropdowns
            day_elem = driver.find_element(By.XPATH, '//*[@id="birthDateDay_0"]')
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", day_elem)
            time.sleep(0.5)
            Select(day_elem).select_by_value(f"{int(d['birth_day']):02d}")
            
            month_elem = driver.find_element(By.XPATH, '//*[@id="birthDateMonth_0"]')
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", month_elem)
            time.sleep(0.5)
            Select(month_elem).select_by_value(f"{int(d['birth_month']):02d}")
            
            year_elem = driver.find_element(By.XPATH, '//*[@id="birthDateYear_0"]')
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", year_elem)
            time.sleep(0.5)
            Select(year_elem).select_by_value(str(d['birth_year']))
            logging.info("Birth date entered")
            
            driver.find_element(By.XPATH, '//*[@id="passportNoAll_0"]').send_keys(d['passport_number'])
            logging.info("Passport number entered")
            
            # Scroll and select passport expiry dropdowns
            passport_day = driver.find_element(By.XPATH, '//*[@id="passportDay_0"]')
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", passport_day)
            time.sleep(0.5)
            Select(passport_day).select_by_value(f"{int(d['passport_exp_day']):02d}")
            
            passport_month = driver.find_element(By.XPATH, '//*[@id="passportMonth_0"]')
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", passport_month)
            time.sleep(0.5)
            Select(passport_month).select_by_value(f"{int(d['passport_exp_month']):02d}")
            
            passport_year = driver.find_element(By.XPATH, '//*[@id="passportYear_0"]')
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", passport_year)
            time.sleep(0.5)
            Select(passport_year).select_by_value(str(d['passport_exp_year']))
            logging.info("Passport expiry date entered")
            
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.searchable-select__selection'))).click()
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.searchable-select__search'))).send_keys(d['nationality'])
            wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'searchable-select__option') and text()='{d['nationality']}']"))).click()
            logging.info("Nationality selected")
        except Exception as e:
            logging.error(f"Failed to fill passenger details: {str(e)}")
            raise
    
    def select_comfort_package(self, wait):
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'provider-package__select') and .//p[text()='Comfort']]"))).click()
            logging.info("Comfort package selected")
        except Exception as e:
            logging.error(f"Failed to select comfort package: {str(e)}")
            raise
    
    def tearDown(self):
        if self.driver:
            try:
                self.driver.quit()
                logging.info("Browser closed")
            except Exception as e:
                logging.error(f"Failed to close browser: {str(e)}")


if __name__ == "__main__":
    import sys
    
    args, unknown = parse_command_line_args()
    
    AviasalesFlightBookingTest.USE_BROWSERSTACK = not args.local
    AviasalesFlightBookingTest.BROWSER = args.browser
    AviasalesFlightBookingTest.OS_TYPE = args.os
    AviasalesFlightBookingTest.EXCEL_FILE_PATH = args.excel
    
    validate_browser_os_combination(args.browser, args.os)
    
    logging.info("=" * 60)
    logging.info("TEST CONFIGURATION")
    logging.info("=" * 60)
    logging.info(f"BrowserStack: {AviasalesFlightBookingTest.USE_BROWSERSTACK}")
    logging.info(f"Browser: {args.browser.upper()}")
    logging.info(f"OS: {args.os.upper()}")
    logging.info(f"Excel: {args.excel}")
    logging.info("=" * 60)
    
    sys.argv = [sys.argv[0]] + unknown
    unittest.main()
