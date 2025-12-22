"""
Script to fetch all test-ids and selectors from Reddit login page
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def fetch_selectors():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    
    try:
        driver.get("https://www.reddit.com/login")
        time.sleep(3)
        
        print("=" * 80)
        print("REDDIT LOGIN PAGE SELECTORS")
        print("=" * 80)
        
        # Find all elements with data-testid
        print("\n--- Elements with data-testid ---")
        testid_elements = driver.find_elements(By.CSS_SELECTOR, "[data-testid]")
        for elem in testid_elements:
            testid = elem.get_attribute("data-testid")
            tag = elem.tag_name
            text = elem.text[:50] if elem.text else ""
            print(f"  data-testid='{testid}' | tag: {tag} | text: {text}")
        
        # Find username field and all its attributes
        print("\n--- Username/Email Input Field ---")
        username_selectors = [
            (By.ID, "loginUsername"),
            (By.NAME, "username"),
            (By.CSS_SELECTOR, "input[placeholder*='Email']"),
            (By.CSS_SELECTOR, "input[placeholder*='email']"),
            (By.CSS_SELECTOR, "input[placeholder*='имя']"),
            (By.CSS_SELECTOR, "input[placeholder*='Электронная почта']"),
            (By.XPATH, "//input[@type='text']"),
            (By.XPATH, "//input[@type='email']"),
        ]
        
        for by, selector in username_selectors:
            try:
                elem = driver.find_element(by, selector)
                print(f"\n  Found by {by}: {selector}")
                print(f"    ID: {elem.get_attribute('id')}")
                print(f"    Name: {elem.get_attribute('name')}")
                print(f"    Type: {elem.get_attribute('type')}")
                print(f"    Placeholder: {elem.get_attribute('placeholder')}")
                print(f"    Class: {elem.get_attribute('class')}")
                print(f"    Data-testid: {elem.get_attribute('data-testid')}")
                print(f"    Aria-label: {elem.get_attribute('aria-label')}")
            except:
                print(f"  Not found by {by}: {selector}")
        
        # Find password field and all its attributes
        print("\n--- Password Input Field ---")
        password_selectors = [
            (By.ID, "loginPassword"),
            (By.NAME, "password"),
            (By.CSS_SELECTOR, "input[type='password']"),
            (By.CSS_SELECTOR, "input[type='password'][placeholder*='Password']"),
            (By.CSS_SELECTOR, "input[type='password'][placeholder*='Пароль']"),
        ]
        
        for by, selector in password_selectors:
            try:
                elem = driver.find_element(by, selector)
                print(f"\n  Found by {by}: {selector}")
                print(f"    ID: {elem.get_attribute('id')}")
                print(f"    Name: {elem.get_attribute('name')}")
                print(f"    Type: {elem.get_attribute('type')}")
                print(f"    Placeholder: {elem.get_attribute('placeholder')}")
                print(f"    Class: {elem.get_attribute('class')}")
                print(f"    Data-testid: {elem.get_attribute('data-testid')}")
                print(f"    Aria-label: {elem.get_attribute('aria-label')}")
            except:
                print(f"  Not found by {by}: {selector}")
        
        # Find login button - try many selectors
        print("\n--- Login Button - Trying Multiple Selectors ---")
        button_selectors = [
            (By.CSS_SELECTOR, "button[type='submit']"),
            (By.XPATH, "//button[contains(text(), 'Войти')]"),
            (By.XPATH, "//button[contains(text(), 'Log in')]"),
            (By.XPATH, "//button[contains(text(), 'Login')]"),
            (By.XPATH, "//button[normalize-space(text())='Войти']"),
            (By.XPATH, "//button[normalize-space(text())='Log in']"),
            (By.CSS_SELECTOR, "button[data-testid*='login']"),
            (By.CSS_SELECTOR, "button[data-testid*='submit']"),
            (By.CSS_SELECTOR, "button[data-testid*='button']"),
            (By.XPATH, "//form//button"),
            (By.XPATH, "//button[@type='submit']"),
            (By.CSS_SELECTOR, "form button"),
            (By.XPATH, "//button[contains(@class, 'login')]"),
            (By.XPATH, "//button[contains(@class, 'submit')]"),
        ]
        
        found_buttons = []
        for by, selector in button_selectors:
            try:
                elem = driver.find_element(by, selector)
                print(f"\n  ✓ Found by {by}: {selector}")
                print(f"    ID: {elem.get_attribute('id')}")
                print(f"    Type: {elem.get_attribute('type')}")
                print(f"    Text: '{elem.text}'")
                print(f"    Inner HTML: {elem.get_attribute('innerHTML')[:100]}")
                print(f"    Class: {elem.get_attribute('class')}")
                print(f"    Data-testid: {elem.get_attribute('data-testid')}")
                print(f"    Aria-label: {elem.get_attribute('aria-label')}")
                print(f"    Is displayed: {elem.is_displayed()}")
                print(f"    Is enabled: {elem.is_enabled()}")
                found_buttons.append((by, selector, elem))
            except Exception as e:
                print(f"  ✗ Not found by {by}: {selector}")
        
        if found_buttons:
            print(f"\n  Total buttons found: {len(found_buttons)}")
            print("  Recommended selector (first found):")
            by, selector, elem = found_buttons[0]
            print(f"    {by}: {selector}")
        
        # Get all input fields
        print("\n--- All Input Fields on Page ---")
        all_inputs = driver.find_elements(By.TAG_NAME, "input")
        for i, inp in enumerate(all_inputs, 1):
            print(f"\n  Input #{i}:")
            print(f"    ID: {inp.get_attribute('id')}")
            print(f"    Name: {inp.get_attribute('name')}")
            print(f"    Type: {inp.get_attribute('type')}")
            print(f"    Placeholder: {inp.get_attribute('placeholder')}")
            print(f"    Class: {inp.get_attribute('class')}")
            print(f"    Data-testid: {inp.get_attribute('data-testid')}")
        
        # Get all buttons with detailed info
        print("\n--- All Buttons on Page (Detailed) ---")
        all_buttons = driver.find_elements(By.TAG_NAME, "button")
        print(f"Total buttons found: {len(all_buttons)}")
        for i, btn in enumerate(all_buttons, 1):
            print(f"\n  Button #{i}:")
            print(f"    ID: {btn.get_attribute('id')}")
            print(f"    Name: {btn.get_attribute('name')}")
            print(f"    Type: {btn.get_attribute('type')}")
            print(f"    Text: '{btn.text}'")
            print(f"    Inner HTML: {btn.get_attribute('innerHTML')[:150]}")
            print(f"    Class: {btn.get_attribute('class')}")
            print(f"    Data-testid: {btn.get_attribute('data-testid')}")
            print(f"    Aria-label: {btn.get_attribute('aria-label')}")
            print(f"    Is displayed: {btn.is_displayed()}")
            print(f"    Is enabled: {btn.is_enabled()}")
            print(f"    Location: {btn.location}")
            print(f"    Size: {btn.size}")
            
            # Try to find by various selectors
            btn_id = btn.get_attribute('id')
            btn_class = btn.get_attribute('class')
            btn_text = btn.text.strip()
            
            if btn_id:
                print(f"    Selector by ID: By.ID, '{btn_id}'")
            if btn_class:
                classes = btn_class.split()
                for cls in classes[:3]:  # First 3 classes
                    print(f"    Selector by class: By.CSS_SELECTOR, 'button.{cls}'")
            if btn_text:
                print(f"    Selector by text: By.XPATH, \"//button[contains(text(), '{btn_text[:20]}')]\"")
        
        print("\n" + "=" * 80)
        time.sleep(5)  # Wait 5 seconds instead of input()
        
    finally:
        driver.quit()

if __name__ == "__main__":
    fetch_selectors()

