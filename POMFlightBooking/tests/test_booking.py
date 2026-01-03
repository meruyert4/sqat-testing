import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from POMFlightBooking.pages.home_page import HomePage
from POMFlightBooking.pages.search_results_page import SearchResultsPage
from POMFlightBooking.pages.booking_page import BookingPage


class TestBooking(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install())
        )
        self.driver.maximize_window()
        
        # Initialize page objects
        self.home_page = HomePage(self.driver)
        self.search_results_page = SearchResultsPage(self.driver)
        self.booking_page = BookingPage(self.driver)

    def test_booking_flow(self):
        # Open homepage and search for flights
        self.home_page.open()
        self.home_page.search_flights("Астана", "Уральск")
        
        # Select ticket from search results
        self.search_results_page.wait_for_results()
        self.search_results_page.select_first_ticket()
        self.search_results_page.click_buy_button()
        
        # Fill booking form
        self.booking_page.fill_booking_form(
            email="23232323@astanait.edu.kz",
            phone="7787296919",
            name="Meruyert",
            lastname="Boranbay",
            birth_day=2,
            birth_month=7,
            birth_year=2005,
            passport_number="123456798",
            passport_exp_day=12,
            passport_exp_month=12,
            passport_exp_year=2030,
            nationality="Казахстан"
        )

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
