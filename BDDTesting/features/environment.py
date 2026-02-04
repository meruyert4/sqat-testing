from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait


def before_scenario(context, scenario):
    """Set up browser before each scenario"""
    context.driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install())
    )
    context.driver.maximize_window()
    context.wait = WebDriverWait(context.driver, 20)


def after_scenario(context, scenario):
    """Clean up browser after each scenario"""
    if hasattr(context, 'driver'):
        context.driver.quit()
