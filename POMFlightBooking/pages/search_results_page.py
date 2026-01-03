from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class SearchResultsPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 45)
        
        # Locators
        self.ticket_price_css = 'div[data-test-id="price"]'
        self.buy_button_xpath = '/html/body/div[2]/div/div/div/div/div[2]/div/div[2]/div[3]/div[1]/div[1]/div/div[2]/button'
    
    def wait_for_results(self):
        print("Waiting for redirect to search results page...")
        print(f"Redirected! Current URL: {self.driver.current_url}")
    
    def select_first_ticket(self):
        print("Searching for flights...")
        try:
            ticket_price = self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.ticket_price_css))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ticket_price)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", ticket_price)
            print("Successfully clicked on the first ticket price")
        except Exception as e:
            print(f"Error during search or redirect: {e}")
            print(f"Final URL before fail: {self.driver.current_url}")
            raise
    
    def click_buy_button(self):
        original_window = self.driver.current_window_handle
        
        buy_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, self.buy_button_xpath))
        )
        buy_button.click()
        print("Clicked 'Buy' button for first proposal")
        
        # Wait for new window and switch to it
        WebDriverWait(self.driver, 10).until(EC.number_of_windows_to_be(2))
        for window_handle in self.driver.window_handles:
            if window_handle != original_window:
                self.driver.switch_to.window(window_handle)
                break
        
        print(f"New page title: {self.driver.title}")
