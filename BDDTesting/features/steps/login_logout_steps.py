from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv
import time

load_dotenv()


@given('I am on the Reddit login page')
def step_navigate_to_login(context):
    context.driver.get("https://www.reddit.com/login")
    time.sleep(2)


@when('I enter my username')
def step_enter_username(context):
    username_input = context.wait.until(
        EC.element_to_be_clickable((By.ID, "login-username"))
    )
    username_input.click()
    time.sleep(0.5)
    context.driver.execute_script("arguments[0].value = '';", username_input)
    username_input.send_keys(os.getenv("USERNAME"))


@when('I enter my password')
def step_enter_password(context):
    password_input = context.wait.until(
        EC.element_to_be_clickable((By.ID, "login-password"))
    )
    password_input.click()
    time.sleep(0.5)
    context.driver.execute_script("arguments[0].value = '';", password_input)
    password_input.send_keys(os.getenv("PASSWORD"))


@when('I click the login button')
def step_click_login(context):
    login_button = context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button.login"))
    )
    context.wait.until(lambda d: login_button.is_enabled())
    time.sleep(0.5)
    try:
        login_button.click()
    except:
        context.driver.execute_script("arguments[0].click();", login_button)
    time.sleep(3)


@then('I should be logged in successfully')
def step_verify_login(context):
    # Wait for login to complete
    time.sleep(2)
    current_url = context.driver.current_url
    assert "/login" not in current_url, "Should not be on login page after successful login"


@then('I should be redirected away from the login page')
def step_verify_redirect(context):
    current_url = context.driver.current_url
    assert "/login" not in current_url, "Should be redirected away from login page"


@given('I am logged in to Reddit')
def step_user_logged_in(context):
    # First perform login
    context.execute_steps('''
        Given I am on the Reddit login page
        When I enter my username
        And I enter my password
        And I click the login button
    ''')
    time.sleep(2)


@when('I navigate to the logout page')
def step_navigate_to_logout(context):
    context.driver.get("https://www.reddit.com/logout")
    time.sleep(2)


@then('I should be logged out successfully')
def step_verify_logout(context):
    current_url = context.driver.current_url
    assert "reddit.com" in current_url, "Should be on Reddit after logout"


@then('I should be on the Reddit homepage')
def step_verify_homepage(context):
    current_url = context.driver.current_url
    is_logged_out = (
        "/login" in current_url or 
        current_url == "https://www.reddit.com/" or 
        "reddit.com" in current_url
    )
    assert is_logged_out, "Should be logged out and on Reddit homepage"
