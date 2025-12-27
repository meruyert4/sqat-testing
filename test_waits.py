import unittest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


@allure.feature("GitHub Waits Test")
class TestGitHubWaits(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

        # implicit Wait
        self.driver.implicitly_wait(10)
        self.driver.get("https://github.com/explore")

    def tearDown(self):
        self.driver.quit()

    @allure.story("Using Implicit, Explicit and Fluent waits")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_github_waits(self):
        driver = self.driver

        # explicit wait
        with allure.step("Explicit wait for 'Trending' link to be clickable and navigate"):
            trending_link = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Trending"))
            )
            trending_link.click()

        # fluent wait
        with allure.step("Fluent wait for trending repository list with polling and ignored exception"):
            fluent_wait = WebDriverWait(
                driver,
                timeout=20,
                poll_frequency=1,
                ignored_exceptions=[NoSuchElementException]
            )
            # wait for trending repository rows to appear
            results = fluent_wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.Box-row"))
            )

        # verify we have at least one trending repository row
        self.assertGreater(len(results), 0)
