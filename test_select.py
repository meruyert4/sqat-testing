import unittest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.feature("Select Dropdown Pattern Test")
class TestSelectDropdown(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

        self.driver.get("https://the-internet.herokuapp.com/dropdown")

    def tearDown(self):
        self.driver.quit()

    @allure.story("Testing native <select> dropdown interactions using Selenium Select class")
    @allure.severity(allure.severity_level.NORMAL)
    def test_select_dropdown_interactions(self):
        driver = self.driver

        with allure.step("Wait for dropdown to be present on page"):
            dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "dropdown"))
            )

        select = Select(dropdown)

        # using select by visible
        with allure.step("Select option by visible text: Option 1"):
            select.select_by_visible_text("Option 1")
            self.assertEqual(select.first_selected_option.text.strip(), "Option 1")

        # using select by value 
        with allure.step("Select option by value: 2 (Option 2)"):
            select.select_by_value("2")
            self.assertEqual(
                select.first_selected_option.get_attribute("value").strip(),
                "2"
            )

        # using select by index
        with allure.step("Select option by index: first option (index 1)"):
            select.select_by_index(1)
            self.assertEqual(select.first_selected_option.text.strip(), "Option 1")



