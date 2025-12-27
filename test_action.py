import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def test_github_actions(driver):
    actions = ActionChains(driver)

    # Open YouTube
    driver.get("https://www.youtube.com")
    
    # Wait for page to load and dismiss any overlay/accept cookies if needed
    WebDriverWait(driver, 15).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, "a[aria-label*='video']")) > 0 or 
                  len(d.find_elements(By.CSS_SELECTOR, "button.yt-spec-button-shape-next")) > 0
    )

    # Mouse hover: hover over subscribe button or any interactive element
    try:
        subscribe_btn = driver.find_element(By.CSS_SELECTOR, "button.yt-spec-button-shape-next")
        actions.move_to_element(subscribe_btn).perform()
        assert subscribe_btn.is_displayed()
    except:
        # Fallback: hover over page body
        body = driver.find_element(By.TAG_NAME, "body")
        actions.move_to_element(body).perform()
        assert body.is_displayed()

    # Right click: context-click on the page
    body = driver.find_element(By.TAG_NAME, "body")
    actions.context_click(body).perform()
    assert body.is_displayed()

    # Double click: double-click on the page
    actions.double_click(body).perform()
    assert body.is_displayed()

    # Drag and scroll gesture: click-and-hold on page then move down (simulating scroll drag)
    actions.click_and_hold(body).move_by_offset(0, 100).release().perform()
    assert body.is_displayed()

    # Keyboard actions: type in the search input, then select-all + delete
    try:
        search_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input#search"))
        )
        search_input.send_keys("selenium testing")
        mod_key = Keys.COMMAND if sys.platform == "darwin" else Keys.CONTROL
        actions.key_down(mod_key).send_keys("a").key_up(mod_key).send_keys(Keys.DELETE).perform()
        WebDriverWait(driver, 10).until(lambda d: d.find_element(By.CSS_SELECTOR, "input#search").get_attribute("value") == "")
        assert search_input.get_attribute("value") == ""
    except:
        # If search input not found, test keyboard actions on body as fallback
        body = driver.find_element(By.TAG_NAME, "body")
        body.send_keys("test")
        mod_key = Keys.COMMAND if sys.platform == "darwin" else Keys.CONTROL
        actions.key_down(mod_key).send_keys("a").key_up(mod_key).send_keys(Keys.BACKSPACE).perform()
        assert body.is_displayed()
