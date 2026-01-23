"""
Aviasales Flight Booking Automation Test
This test automates the flight booking process on Aviasales website.

Features:
- Reads test data from Excel file (using openpyxl)
- Supports local and remote execution (BrowserStack)
- Supports multiple browsers (Chrome, Firefox)
- Configurable via Excel file
"""

import unittest
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Import our Excel reader module
from excel_reader import read_test_data, get_browserstack_config


class AviasalesFlightBookingTest(unittest.TestCase):
    """
    Test class for Aviasales flight booking automation.
    """
    
    # Class variables for configuration
    USE_BROWSERSTACK = False  # Set to True to use BrowserStack
    BROWSER = "Chrome"  # Options: "Chrome" or "Firefox"
    EXCEL_FILE_PATH = "test_data.xlsx"  # Path to Excel file with test data
    
    def setUp(self):
        """
        Setup method - runs before each test.
        Initializes the WebDriver (local or remote).
        """
        print("\n" + "="*60)
        print("SETUP: Initializing WebDriver...")
        print("="*60)
        
        # Read test data from Excel
        self.test_data = self.load_test_data_from_excel()
        
        # Initialize driver based on configuration
        if self.USE_BROWSERSTACK:
            self.driver = self.setup_browserstack_driver()
        else:
            self.driver = self.setup_local_driver()
        
        # Maximize browser window
        self.driver.maximize_window()
        print("✓ WebDriver initialized successfully")
        print(f"✓ Using browser: {self.BROWSER}")
        print(f"✓ Execution mode: {'BrowserStack (Remote)' if self.USE_BROWSERSTACK else 'Local'}")
    
    def load_test_data_from_excel(self):
        """
        Loads test data from Excel file.
        
        Returns:
            dict: Dictionary with test data
        """
        print("\n--- Loading Test Data from Excel ---")
        
        # Check if Excel file exists
        if not os.path.exists(self.EXCEL_FILE_PATH):
            print(f"❌ ERROR: Excel file not found: {self.EXCEL_FILE_PATH}")
            print("Please create the Excel file according to EXCEL_SETUP_INSTRUCTIONS.md")
            raise FileNotFoundError(f"Excel file not found: {self.EXCEL_FILE_PATH}")
        
        # Read test data
        test_data = read_test_data(self.EXCEL_FILE_PATH)
        
        # Validate required fields
        required_fields = [
            'url', 'from_city', 'to_city', 'email', 'phone',
            'name', 'lastname', 'birth_day', 'birth_month', 'birth_year',
            'passport_number', 'passport_exp_day', 'passport_exp_month',
            'passport_exp_year', 'nationality'
        ]
        
        missing_fields = [field for field in required_fields if field not in test_data]
        
        if missing_fields:
            print(f"❌ ERROR: Missing required fields in Excel: {missing_fields}")
            raise ValueError(f"Missing required fields: {missing_fields}")
        
        print("✓ All required test data loaded successfully")
        return test_data
    
    def setup_local_driver(self):
        """
        Sets up local WebDriver (Chrome or Firefox).
        
        Returns:
            WebDriver: Local WebDriver instance
        """
        print("\n--- Setting up Local WebDriver ---")
        
        if self.BROWSER.lower() == "chrome":
            options = ChromeOptions()
            # Add any Chrome options here if needed
            # options.add_argument('--headless')  # Uncomment for headless mode
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )
        elif self.BROWSER.lower() == "firefox":
            options = FirefoxOptions()
            # Add any Firefox options here if needed
            # options.add_argument('--headless')  # Uncomment for headless mode
            driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=options
            )
        else:
            raise ValueError(f"Unsupported browser: {self.BROWSER}")
        
        return driver
    
    def setup_browserstack_driver(self):
        """
        Sets up remote WebDriver for BrowserStack execution.
        
        Returns:
            WebDriver: Remote WebDriver instance connected to BrowserStack
        """
        print("\n--- Setting up BrowserStack Remote WebDriver ---")
        
        # Get BrowserStack configuration from Excel
        capabilities, username, access_key = get_browserstack_config(
            self.EXCEL_FILE_PATH,
            self.BROWSER
        )
        
        # Validate credentials
        if not username or not access_key:
            print("❌ ERROR: BrowserStack credentials not found in Excel file")
            print("Please add username and access_key in BrowserStack sheet")
            raise ValueError("BrowserStack credentials missing")
        
        # BrowserStack Hub URL
        hub_url = f"https://{username}:{access_key}@hub-cloud.browserstack.com/wd/hub"
        
        print(f"✓ Connecting to BrowserStack...")
        print(f"  Browser: {capabilities['browserName']}")
        print(f"  OS: {capabilities['os']} {capabilities['osVersion']}")
        
        # Create remote WebDriver
        driver = webdriver.Remote(
            command_executor=hub_url,
            desired_capabilities=capabilities
        )
        
        print("✓ Connected to BrowserStack successfully")
        return driver
    
    def test_flight_booking_process(self):
        """
        Main test method - Tests the complete flight booking process.
        
        Test Steps:
        1. Open Aviasales website
        2. Disable Booking.com checkbox
        3. Fill search form (from, to, date)
        4. Search for flights
        5. Select a flight
        6. Fill passenger details
        7. Select flight package
        """
        driver = self.driver
        wait = WebDriverWait(driver, 20)
        
        print("\n" + "="*60)
        print("TEST STARTED: Flight Booking Process")
        print("="*60)
        
        # STEP 1: Open Aviasales website
        print("\n[STEP 1] Opening Aviasales website...")
        website_url = self.test_data['url']
        driver.get(website_url)
        print(f"✓ Navigated to: {website_url}")
        time.sleep(2)
        
        # STEP 2: Disable Booking.com checkbox
        print("\n[STEP 2] Handling Booking.com checkbox...")
        self.handle_booking_checkbox(wait)
        
        # STEP 3: Fill search form
        print("\n[STEP 3] Filling search form...")
        self.fill_search_form(wait)
        
        # STEP 4: Search for flights
        print("\n[STEP 4] Searching for flights...")
        self.search_flights(wait)
        
        # STEP 5: Select first flight
        print("\n[STEP 5] Selecting flight...")
        self.select_flight(wait)
        
        # STEP 6: Fill passenger details
        print("\n[STEP 6] Filling passenger details...")
        self.fill_passenger_details(wait)
        
        # STEP 7: Select comfort package
        print("\n[STEP 7] Selecting flight package...")
        self.select_comfort_package(wait)
        
        print("\n" + "="*60)
        print("TEST COMPLETED SUCCESSFULLY ✓")
        print("="*60)
        time.sleep(5)
    
    def handle_booking_checkbox(self, wait):
        """
        Handles the Booking.com checkbox on the homepage.
        
        Args:
            wait: WebDriverWait instance
        """
        try:
            booking_label = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//label[contains(., 'Booking.com')]")
            ))
            
            checkbox_input = booking_label.find_element(By.TAG_NAME, "input")
            
            if checkbox_input.is_selected():
                self.driver.execute_script("arguments[0].click();", booking_label)
                print("✓ Booking.com checkbox was active - disabled it")
            else:
                self.driver.execute_script("arguments[0].click();", booking_label)
                print("✓ Clicked on Booking.com checkbox")
                
        except Exception as e:
            print(f"⚠ Warning: Could not handle Booking checkbox: {e}")
    
    def fill_search_form(self, wait):
        """
        Fills the flight search form with data from Excel.
        
        Args:
            wait: WebDriverWait instance
        """
        driver = self.driver
        
        # Enter departure city
        from_city = self.test_data['from_city']
        from_input = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="avia_form_origin-input"]')
        ))
        from_input.clear()
        from_input.send_keys(from_city)
        print(f"✓ Entered departure city: {from_city}")
        
        # Enter destination city
        to_city = self.test_data['to_city']
        to_input = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="avia_form_destination-input"]')
        ))
        to_input.clear()
        to_input.send_keys(to_city)
        print(f"✓ Entered destination city: {to_city}")
        
        # Open calendar
        date_picker_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/form/div[1]/div[3]/div[1]/div[1]/button[1]')
        ))
        date_picker_button.click()
        print("✓ Opened date picker")
        
        # Select date (28th of the month)
        target_date = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'div.s__vY0Kp_7_YUAgIkqP:nth-child(3) > table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(5) > td:nth-child(3) > div:nth-child(1) > button:nth-child(1) > div:nth-child(2)')
        ))
        target_date.click()
        print("✓ Selected date: 28.02.2025")
        
        # Confirm date selection
        confirm_date_xpath = "//button[contains(., 'Выбрать')] | //button[contains(., 'Готово')] | /html/body/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/form/div[1]/div[3]/div[1]/div[2]/div[1]/div/div/div/div/button"
        
        try:
            confirm_btn = wait.until(EC.element_to_be_clickable((By.XPATH, confirm_date_xpath)))
            confirm_btn.click()
            print("✓ Confirmed date selection")
        except Exception as e:
            print("⚠ No confirm button needed or found")
    
    def search_flights(self, wait):
        """
        Clicks the search button and waits for results.
        
        Args:
            wait: WebDriverWait instance
        """
        driver = self.driver
        
        # Click search button
        search_btn_selector = 'button[data-test-id="form-submit"]'
        
        try:
            search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, search_btn_selector)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_button)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", search_button)
            print("✓ Search button clicked")
            
        except Exception as e:
            print(f"⚠ Trying alternative method to submit search...")
            to_input = driver.find_element(By.XPATH, '//*[@id="avia_form_destination-input"]')
            to_input.send_keys(Keys.ENTER)
        
        # Wait for search results
        print("⏳ Waiting for search results...")
        
        ticket_price_selector = 'div[data-test-id="price"]'
        ticket_price = WebDriverWait(driver, 45).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ticket_price_selector))
        )
        
        print("✓ Search results loaded")
    
    def select_flight(self, wait):
        """
        Selects the first available flight and proceeds to booking.
        
        Args:
            wait: WebDriverWait instance
        """
        driver = self.driver
        
        # Click on first ticket price
        ticket_price_selector = 'div[data-test-id="price"]'
        ticket_price = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ticket_price_selector))
        )
        
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ticket_price)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", ticket_price)
        print("✓ Selected first flight")
        
        # Click buy button
        buy_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/div/div[2]/div/div[2]/div[3]/div[1]/div[1]/div/div[2]/button'))
        )
        
        original_window = driver.current_window_handle
        buy_button.click()
        print("✓ Clicked 'Buy' button")
        
        # Wait for new window and switch to it
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break
        
        print(f"✓ Switched to booking page: {driver.title}")
        time.sleep(2)
    
    def fill_passenger_details(self, wait):
        """
        Fills passenger details form with data from Excel.
        
        Args:
            wait: WebDriverWait instance
        """
        driver = self.driver
        
        # Get passenger data from Excel
        email = str(self.test_data['email'])
        phone = str(self.test_data['phone'])
        name = str(self.test_data['name'])
        lastname = str(self.test_data['lastname'])
        birth_day = int(self.test_data['birth_day'])
        birth_month = int(self.test_data['birth_month'])
        birth_year = int(self.test_data['birth_year'])
        passport_number = str(self.test_data['passport_number'])
        passport_exp_day = int(self.test_data['passport_exp_day'])
        passport_exp_month = int(self.test_data['passport_exp_month'])
        passport_exp_year = int(self.test_data['passport_exp_year'])
        nationality = str(self.test_data['nationality'])
        
        # Fill email
        email_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="contact_email"]')))
        email_input.clear()
        email_input.send_keys(email)
        print(f"✓ Entered email: {email}")
        
        # Fill phone
        phone_input = driver.find_element(By.XPATH, '//*[@id="contact_cellphone"]')
        phone_input.clear()
        phone_input.send_keys(phone)
        print(f"✓ Entered phone: {phone}")
        
        # Fill name
        name_input = driver.find_element(By.XPATH, '//*[@id="firstName_0"]')
        name_input.clear()
        name_input.send_keys(name)
        print(f"✓ Entered first name: {name}")
        
        # Fill lastname
        lastname_input = driver.find_element(By.XPATH, '//*[@id="lastName_0"]')
        lastname_input.clear()
        lastname_input.send_keys(lastname)
        print(f"✓ Entered last name: {lastname}")
        
        # Select gender (female)
        female_label = driver.find_element(By.XPATH, '//*[@id="gender_F_0"]')
        if not female_label.is_selected():
            try:
                close_overlay = driver.find_elements(By.CSS_SELECTOR, '.membership-container [data-testid="closeIcon"]')
                if close_overlay:
                    close_overlay[0].click()
                    WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((By.ID, 'membershipContainer')))
                female_label.click()
            except Exception:
                driver.execute_script("arguments[0].click();", female_label)
        print("✓ Selected gender: Female")
        
        # Fill date of birth
        Select(driver.find_element(By.XPATH, '//*[@id="birthDateDay_0"]')).select_by_value(f"{birth_day:02d}")
        Select(driver.find_element(By.XPATH, '//*[@id="birthDateMonth_0"]')).select_by_value(f"{birth_month:02d}")
        Select(driver.find_element(By.XPATH, '//*[@id="birthDateYear_0"]')).select_by_value(str(birth_year))
        print(f"✓ Entered date of birth: {birth_day:02d}/{birth_month:02d}/{birth_year}")
        
        # Fill passport number
        passport_input = driver.find_element(By.XPATH, '//*[@id="passportNoAll_0"]')
        passport_input.clear()
        passport_input.send_keys(passport_number)
        print(f"✓ Entered passport number: {passport_number}")
        
        # Fill passport expiration
        Select(driver.find_element(By.XPATH, '//*[@id="passportDay_0"]')).select_by_value(f"{passport_exp_day:02d}")
        Select(driver.find_element(By.XPATH, '//*[@id="passportMonth_0"]')).select_by_value(f"{passport_exp_month:02d}")
        Select(driver.find_element(By.XPATH, '//*[@id="passportYear_0"]')).select_by_value(str(passport_exp_year))
        print(f"✓ Entered passport expiration: {passport_exp_day:02d}/{passport_exp_month:02d}/{passport_exp_year}")
        
        # Select nationality
        dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.searchable-select__selection')))
        dropdown.click()
        
        search_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.searchable-select__search')))
        search_input.clear()
        search_input.send_keys(nationality)
        
        option = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//div[contains(@class, 'searchable-select__option') and text()='{nationality}']")
        ))
        option.click()
        print(f"✓ Selected nationality: {nationality}")
        
        print("✓ All passenger details filled successfully")
    
    def select_comfort_package(self, wait):
        """
        Selects the Comfort flight package.
        
        Args:
            wait: WebDriverWait instance
        """
        driver = self.driver
        
        comfort_package = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class, 'provider-package__select') and .//p[text()='Comfort']]")
        ))
        comfort_package.click()
        print("✓ Selected 'Comfort' flight package")
        
        time.sleep(3)
    
    def tearDown(self):
        """
        Cleanup method - runs after each test.
        Closes the browser and ends the session.
        """
        print("\n" + "="*60)
        print("TEARDOWN: Closing browser...")
        print("="*60)
        
        if self.driver:
            self.driver.quit()
            print("✓ Browser closed successfully")


# Test execution configurations
def run_tests_with_config(use_browserstack=False, browser="Chrome"):
    """
    Helper function to run tests with specific configuration.
    
    Args:
        use_browserstack (bool): Whether to use BrowserStack
        browser (str): Browser to use ("Chrome" or "Firefox")
    """
    # Set class variables
    AviasalesFlightBookingTest.USE_BROWSERSTACK = use_browserstack
    AviasalesFlightBookingTest.BROWSER = browser
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(AviasalesFlightBookingTest)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    """
    Main execution block.
    Configure your test execution here.
    """
    
    print("\n" + "="*60)
    print("AVIASALES FLIGHT BOOKING AUTOMATION TEST")
    print("="*60)
    
    # =====================================================
    # CONFIGURATION - Modify these settings as needed
    # =====================================================
    
    # Set to True to use BrowserStack, False for local execution
    USE_REMOTE_EXECUTION = False
    
    # Choose browser: "Chrome" or "Firefox"
    SELECTED_BROWSER = "Chrome"
    
    # =====================================================
    
    print(f"\nConfiguration:")
    print(f"  - Execution Mode: {'BrowserStack (Remote)' if USE_REMOTE_EXECUTION else 'Local'}")
    print(f"  - Browser: {SELECTED_BROWSER}")
    print(f"  - Excel File: test_data.xlsx")
    print("\n")
    
    # Run tests with configuration
    result = run_tests_with_config(
        use_browserstack=USE_REMOTE_EXECUTION,
        browser=SELECTED_BROWSER
    )
    
    # Print summary
    print("\n" + "="*60)
    print("TEST EXECUTION SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success: {result.wasSuccessful()}")
    print("="*60)
