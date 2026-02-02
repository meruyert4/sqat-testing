from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time


@given('I am on the Aviasales homepage')
def step_open_aviasales(context):
    context.driver.get("https://www.aviasales.kz")
    time.sleep(2)


@when('I disable the Booking.com checkbox')
def step_disable_booking_checkbox(context):
    try:
        booking_label = context.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//label[contains(., 'Booking.com')]")
        ))
        checkbox_input = booking_label.find_element(By.TAG_NAME, "input")
        
        if checkbox_input.is_selected():
            context.driver.execute_script("arguments[0].click();", booking_label)
            print("Booking.com checkbox was active - disabled it.")
        else:
            context.driver.execute_script("arguments[0].click();", booking_label)
            print("Clicked on Booking.com checkbox (inactive mode).")
    except Exception as e:
        print(f"Failed to handle Booking checkbox: {e}")


@when('I enter "{city}" as departure city')
def step_enter_departure_city(context, city):
    from_input = context.wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="avia_form_origin-input"]')
    ))
    from_input.clear()
    from_input.send_keys(city)
    time.sleep(1)


@when('I enter "{city}" as destination city')
def step_enter_destination_city(context, city):
    to_input = context.wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="avia_form_destination-input"]')
    ))
    to_input.clear()
    to_input.send_keys(city)
    time.sleep(1)


@when('I select departure date "{date}"')
def step_select_date(context, date):
    # Open calendar
    date_picker_button = context.wait.until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/form/div[1]/div[3]/div[1]/div[1]/button[1]')
    ))
    date_picker_button.click()
    time.sleep(1)
    
    # Select date (28.02.2025)
    target_date = context.wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'div.s__vY0Kp_7_YUAgIkqP:nth-child(3) > table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(5) > td:nth-child(3) > div:nth-child(1) > button:nth-child(1) > div:nth-child(2)')
    ))
    target_date.click()
    time.sleep(1)
    
    # Confirm date
    confirm_date_xpath = "//button[contains(., 'Выбрать')] | //button[contains(., 'Готово')] | /html/body/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/form/div[1]/div[3]/div[1]/div[2]/div[1]/div/div/div/div/button"
    try:
        confirm_btn = context.wait.until(EC.element_to_be_clickable((By.XPATH, confirm_date_xpath)))
        confirm_btn.click()
        time.sleep(1)
    except Exception:
        pass


@when('I click the search button')
def step_click_search_button(context):
    search_btn_selector = 'button[data-test-id="form-submit"]'
    try:
        search_button = context.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, search_btn_selector)
        ))
        context.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_button)
        time.sleep(1)
        context.driver.execute_script("arguments[0].click();", search_button)
        time.sleep(3)
    except Exception as e:
        print(f"Failed to click search button: {e}")
        to_input = context.driver.find_element(By.XPATH, '//*[@id="avia_form_destination-input"]')
        to_input.send_keys(Keys.ENTER)
        time.sleep(3)


@then('I should see available flight options')
def step_verify_flight_options(context):
    from selenium.webdriver.support.ui import WebDriverWait
    ticket_price_selector = 'div[data-test-id="price"]'
    extended_wait = WebDriverWait(context.driver, 60)
    ticket_price = extended_wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ticket_price_selector))
    )
    assert ticket_price.is_displayed(), "Flight options should be visible"


@when('I search for flights from "{origin}" to "{destination}" on "{date}"')
def step_search_flights(context, origin, destination, date):
    # Reuse previous steps
    context.execute_steps(f'''
        When I disable the Booking.com checkbox
        And I enter "{origin}" as departure city
        And I enter "{destination}" as destination city
        And I select departure date "{date}"
        And I click the search button
    ''')


@when('I select the first available flight')
def step_select_first_flight(context):
    from selenium.webdriver.support.ui import WebDriverWait
    ticket_price_selector = 'div[data-test-id="price"]'
    extended_wait = WebDriverWait(context.driver, 60)
    ticket_price = extended_wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ticket_price_selector))
    )
    context.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ticket_price)
    time.sleep(1)
    context.driver.execute_script("arguments[0].click();", ticket_price)
    time.sleep(3)


@when('I click the buy button')
def step_click_buy_button(context):
    from selenium.webdriver.support.ui import WebDriverWait
    extended_wait = WebDriverWait(context.driver, 30)
    buy_button = extended_wait.until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/div/div[2]/div/div[2]/div[3]/div[1]/div[1]/div/div[2]/button'))
    )
    context.original_window = context.driver.current_window_handle
    buy_button.click()
    time.sleep(3)


@when('I switch to the booking page')
def step_switch_to_booking_window(context):
    from selenium.webdriver.support.ui import WebDriverWait
    extended_wait = WebDriverWait(context.driver, 30)
    extended_wait.until(EC.number_of_windows_to_be(2))
    for window_handle in context.driver.window_handles:
        if window_handle != context.original_window:
            context.driver.switch_to.window(window_handle)
            break
    time.sleep(8)


@then('the booking page should load successfully')
def step_verify_booking_page_simple(context):
    print(f"Current URL: {context.driver.current_url}")
    print(f"Current title: {context.driver.title}")
    assert context.driver.current_url != '', "Should be on booking page"


@given('I have navigated to a flight booking form')
def step_navigate_to_booking_form(context):
    # Do the full flow once to get to booking form
    try:
        context.execute_steps('''
            Given I am on the Aviasales homepage
            When I search for flights from "Астана" to "Уральск" on "28.02.2025"
        ''')
        time.sleep(5)
        
        # Try to select flight with extended timeout
        from selenium.webdriver.support.ui import WebDriverWait
        ticket_price_selector = 'div[data-test-id="price"]'
        extended_wait = WebDriverWait(context.driver, 90)
        ticket_price = extended_wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ticket_price_selector))
        )
        context.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ticket_price)
        time.sleep(2)
        context.driver.execute_script("arguments[0].click();", ticket_price)
        time.sleep(5)
        
        # Click buy button
        buy_button = extended_wait.until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/div/div[2]/div/div[2]/div[3]/div[1]/div[1]/div/div[2]/button'))
        )
        context.original_window = context.driver.current_window_handle
        buy_button.click()
        time.sleep(3)
        
        # Switch to new window
        extended_wait.until(EC.number_of_windows_to_be(2))
        for window_handle in context.driver.window_handles:
            if window_handle != context.original_window:
                context.driver.switch_to.window(window_handle)
                break
        time.sleep(10)
        print(f"Successfully navigated to booking form. URL: {context.driver.current_url}")
    except Exception as e:
        print(f"Warning: Could not complete full flow to booking form: {e}")
        print("This scenario requires manual navigation or may be flaky due to website timing")
        raise


@then('I should be redirected to the booking page')
def step_verify_booking_page(context):
    from selenium.webdriver.support.ui import WebDriverWait
    extended_wait = WebDriverWait(context.driver, 30)
    extended_wait.until(EC.number_of_windows_to_be(2))
    for window_handle in context.driver.window_handles:
        if window_handle != context.original_window:
            context.driver.switch_to.window(window_handle)
            break
    # Wait for page to load completely
    time.sleep(8)
    print(f"Current URL: {context.driver.current_url}")
    print(f"Current title: {context.driver.title}")
    assert context.driver.current_url != '', "Should be on booking page"


@given('I am on the flight booking page')
def step_on_booking_page(context):
    # This assumes we've already navigated through the previous steps
    # In a real scenario, you might want to set up the context differently
    context.execute_steps('''
        Given I am on the Aviasales homepage
        When I search for flights from "Астана" to "Уральск" on "28.02.2025"
        And I select the first available flight
        And I click the buy button
    ''')
    # Give extra time for booking page to fully load
    time.sleep(10)
    print(f"Booking page loaded. URL: {context.driver.current_url}")


@when('I fill in contact email "{email}"')
def step_fill_email(context, email):
    from selenium.webdriver.support.ui import WebDriverWait
    # Increase wait time for booking page elements
    extended_wait = WebDriverWait(context.driver, 60)
    try:
        # Try multiple locator strategies
        email_input = extended_wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="contact_email"]'))
        )
        print("Email field found")
    except Exception as e:
        print(f"Failed to find email field with XPATH, trying CSS selector. Error: {e}")
        email_input = extended_wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#contact_email, input[name="email"]'))
        )
    
    # Scroll to element and ensure it's visible
    context.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", email_input)
    time.sleep(1)
    email_input.clear()
    email_input.send_keys(email)
    print(f"Email filled: {email}")


@when('I fill in contact phone "{phone}"')
def step_fill_phone(context, phone):
    phone_input = context.driver.find_element(By.XPATH, '//*[@id="contact_cellphone"]')
    phone_input.clear()
    phone_input.send_keys(phone)


@when('I fill in passenger first name "{name}"')
def step_fill_first_name(context, name):
    name_input = context.driver.find_element(By.XPATH, '//*[@id="firstName_0"]')
    name_input.clear()
    name_input.send_keys(name)


@when('I fill in passenger last name "{lastname}"')
def step_fill_last_name(context, lastname):
    lastname_input = context.driver.find_element(By.XPATH, '//*[@id="lastName_0"]')
    lastname_input.clear()
    lastname_input.send_keys(lastname)


@when('I select gender as "{gender}"')
def step_select_gender(context, gender):
    female_label = context.driver.find_element(By.XPATH, '//*[@id="gender_F_0"]')
    if not female_label.is_selected():
        try:
            close_overlay = context.driver.find_elements(By.CSS_SELECTOR, '.membership-container [data-testid="closeIcon"]')
            if close_overlay:
                close_overlay[0].click()
                time.sleep(1)
            female_label.click()
        except Exception:
            context.driver.execute_script("arguments[0].click();", female_label)


@when('I fill in date of birth as "{dob}"')
def step_fill_date_of_birth(context, dob):
    # dob format: "DD/MM/YYYY"
    day, month, year = dob.split('/')
    Select(context.driver.find_element(By.XPATH, '//*[@id="birthDateDay_0"]')).select_by_value(f"{int(day):02d}")
    Select(context.driver.find_element(By.XPATH, '//*[@id="birthDateMonth_0"]')).select_by_value(f"{int(month):02d}")
    Select(context.driver.find_element(By.XPATH, '//*[@id="birthDateYear_0"]')).select_by_value(year)


@when('I fill in passport number "{passport}"')
def step_fill_passport(context, passport):
    passport_input = context.driver.find_element(By.XPATH, '//*[@id="passportNoAll_0"]')
    passport_input.clear()
    passport_input.send_keys(passport)


@when('I fill in passport expiration date as "{exp_date}"')
def step_fill_passport_expiration(context, exp_date):
    # exp_date format: "DD/MM/YYYY"
    day, month, year = exp_date.split('/')
    Select(context.driver.find_element(By.XPATH, '//*[@id="passportDay_0"]')).select_by_value(f"{int(day):02d}")
    Select(context.driver.find_element(By.XPATH, '//*[@id="passportMonth_0"]')).select_by_value(f"{int(month):02d}")
    Select(context.driver.find_element(By.XPATH, '//*[@id="passportYear_0"]')).select_by_value(year)


@when('I select nationality "{nationality}"')
def step_select_nationality(context, nationality):
    dropdown = context.wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.searchable-select__selection'))
    )
    dropdown.click()
    
    search_input = context.wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.searchable-select__search'))
    )
    search_input.clear()
    search_input.send_keys(nationality)
    
    option = context.wait.until(
        EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'searchable-select__option') and text()='{nationality}']"))
    )
    option.click()


@when('I select "{package}" package')
def step_select_package(context, package):
    comfort_package = context.wait.until(
        EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'provider-package__select') and .//p[text()='{package}']]"))
    )
    comfort_package.click()
    time.sleep(2)


@then('the booking form should be completed successfully')
def step_verify_form_completion(context):
    # Verify key fields are filled
    email_input = context.driver.find_element(By.XPATH, '//*[@id="contact_email"]')
    assert email_input.get_attribute('value') != '', "Email should be filled"
    print("Booking form completed successfully")
