
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


class AviasalesOpenTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install())
        )
        self.driver.maximize_window()

    def test_open_aviasales(self):
        driver = self.driver
        # 1. Переходим на главную страницу вместо прямой ссылки на поиск
        driver.get("https://www.aviasales.kz")
        wait = WebDriverWait(driver, 20)

        print("удаляем галочку")

        # Находим контейнер, в котором лежит эта галочка (например, страховка или доп. услуга)
        try:
            # 1. Ищем label, который содержит текст "Booking.com"
            # Это самый надежный способ, так как текст меняется редко
            booking_label = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//label[contains(., 'Booking.com')]")
            ))

            # 2. Ищем сам input внутри этого label
            checkbox_input = booking_label.find_element(By.TAG_NAME, "input")

            # 3. Проверяем: если чекбокс выбран (is_selected), то кликаем по нему, чтобы выключить
            # Если на сайте кастомный чекбокс, и is_selected() всегда возвращает False,
            # мы можем просто кликнуть по нему один раз, чтобы гарантированно его "снять"
            if checkbox_input.is_selected():
                driver.execute_script("arguments[0].click();", booking_label)
                print("Галочка Booking.com была активна — выключили.")
            else:
                # На Aviasales этот чекбокс часто включен по умолчанию, 
                # но визуально input может не показывать статус. 
                # Если ты видишь, что он все равно остается включенным, просто используй:
                driver.execute_script("arguments[0].click();", booking_label)
                print("Нажали на чекбокс Booking.com (inactive mode).")

        except Exception as e:
            print(f"Не удалось обработать чекбокс Booking: {e}")

        print("Filling search form...")

        # 2. Вводим город отправления (Нур-Султан / NQZ)
        from_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="avia_form_origin-input"]')))
        from_input.clear() # На всякий случай очищаем
        from_input.send_keys("Астана")
        
        # 3. Вводим город прибытия (Уральск / URA)
        to_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="avia_form_destination-input"]')))
        to_input.clear()
        to_input.send_keys("Уральск")

        # 4. Открываем календарь
        date_picker_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/form/div[1]/div[3]/div[1]/div[1]/button[1]')))
        date_picker_button.click()

        # Используем CSS-селектор для data-test-id, так как это надежнее классов
        target_date = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.s__vY0Kp_7_YUAgIkqP:nth-child(3) > table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(5) > td:nth-child(3) > div:nth-child(1) > button:nth-child(1) > div:nth-child(2)')))
        target_date.click()
        print("Date selected: 28.02.2025")

        # --- 6. Нажимаем кнопку подтверждения даты ---
        confirm_date_xpath = "//button[contains(., 'Выбрать')] | //button[contains(., 'Готово')] | /html/body/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/form/div[1]/div[3]/div[1]/div[2]/div[1]/div/div/div/div/button"
        
        original_window = driver.current_window_handle
        
        try:
            confirm_btn = wait.until(EC.element_to_be_clickable((By.XPATH, confirm_date_xpath)))
            confirm_btn.click()
            print("Confirm button clicked")
        except Exception as e:
            print("No new tab or confirm button issues, staying on current page.")

       

       # --- 7. Нажимаем "Найти билеты" ---
        print("Looking for search button...")
        
        # Используем максимально надежный селектор по data-test-id
        search_btn_selector = 'button[data-test-id="form-submit"]'
        
        try:
            # Ждем появления кнопки
            search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, search_btn_selector)))
            
            # Прокрутим к ней, чтобы она была в поле зрения
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_button)
            time.sleep(1) # Даем секунду на завершение анимации
            
            # Кликаем через JavaScript (игнорирует невидимые перекрытия)
            driver.execute_script("arguments[0].click();", search_button)
            print("Search button clicked via JS!")
            
        except Exception as e:
            print(f"Failed to click search button: {e}")
            # План Б: если кнопка не нажалась, попробуем нажать Enter в поле ввода "Куда"
            print("Trying Plan B: Pressing ENTER in destination field...")
            to_input = driver.find_element(By.XPATH, '//*[@id="avia_form_destination-input"]')
            to_input.send_keys(Keys.ENTER)

        # --- 8. Ожидание редиректа и результатов поиска ---
        print("Waiting for redirect to search results page...")
        
        try:
            # 1. Ждем, пока URL изменится на поисковый
            # Это гарантирует, что драйвер понимает: мы на новой странице
            WebDriverWait(driver, 15).until(EC.url_contains("/search/"))
            print(f"Redirected! Current URL: {driver.current_url}")

            # 2. Ждем, пока исчезнет лоадер (полоска загрузки сверху), если он есть
            # Или просто ждем появления первого билета с ценой
            # Увеличиваем время, так как поиск реально может идти долго
            print("Searching for flights...")
            
            # Используем селектор для цены, так как это главный признак загрузки билета
            ticket_price_selector = 'div[data-test-id="price"]'
            
            ticket_price = WebDriverWait(driver, 45).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ticket_price_selector))
            )
            
            # 3. Прокрутка и клик
            # Важно: на поисковой странице часто всплывают подсказки, 
            # поэтому JS-клик здесь — самый безопасный вариант
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ticket_price)
            time.sleep(1) # пауза для прогрузки интерфейса
            
            driver.execute_script("arguments[0].click();", ticket_price)
            print("Successfully clicked on the first ticket price")

        except Exception as e:
            print(f"Error during search or redirect: {e}")
            print(f"Final URL before fail: {driver.current_url}")
            raise # Останавливаем тест, если не нашли билеты

        # Wait for the module to appear and then click the 'Купить' button for the first proposal
        buy_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/div/div[2]/div/div[2]/div[3]/div[1]/div[1]/div/div[2]/button'))
        )
        
        # 1. Save the handle of the current (Aviasales) window
        original_window = driver.current_window_handle

        buy_button.click() # Here it redirects to another website to pay
        print("Clicked 'Купить' button for first proposal")

        # 3. Wait for the new window or tab to open
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

        # 4. Loop through handles to find the new one
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break

        # Now the 'driver' is focused on the airline/booking website
        print(f"New page title: {driver.title}")

        # Fill booking form fields using XPaths and values
        email = "example@astanait.edu.kz"
        phone = "7787296919"
        name = "Meruyert"
        lastname = "Boranbay"
        birth_day = 2
        birth_month = 7
        birth_year = 2005
        passport_number = "123456798"
        passport_exp_day = 15
        passport_exp_month = 3
        passport_exp_year = 2032
        natianalaty="Россия"

        # Email
        email_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="contact_email"]'))
        )
        email_input.clear()
        email_input.send_keys(email)

        # Phone
        phone_input = driver.find_element(By.XPATH, '//*[@id="contact_cellphone"]')
        phone_input.clear()
        phone_input.send_keys(phone)

        # Name
        name_input = driver.find_element(By.XPATH, '//*[@id="firstName_0"]')
        name_input.clear()
        name_input.send_keys(name)

        # Lastname
        lastname_input = driver.find_element(By.XPATH, '//*[@id="lastName_0"]')
        lastname_input.clear()
        lastname_input.send_keys(lastname)


        # Sex (male) - handle overlay if present
        male_label = driver.find_element(By.XPATH, '//*[@id="gender_M_0"]')
        if not male_label.is_selected():
            try:
                # Try to close overlay if it exists
                close_overlay = driver.find_elements(By.CSS_SELECTOR, '.membership-container [data-testid="closeIcon"]')
                if close_overlay:
                    close_overlay[0].click()
                    WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((By.ID, 'membershipContainer')))
                male_label.click()
            except Exception:
                # If still not clickable, use JS click
                driver.execute_script("arguments[0].click();", male_label)

        # Date of birth
        from selenium.webdriver.support.ui import Select
        Select(driver.find_element(By.XPATH, '//*[@id="birthDateDay_0"]')).select_by_value(f"{birth_day:02d}")
        Select(driver.find_element(By.XPATH, '//*[@id="birthDateMonth_0"]')).select_by_value(f"{birth_month:02d}")
        Select(driver.find_element(By.XPATH, '//*[@id="birthDateYear_0"]')).select_by_value(str(birth_year))

        # Passport number
        passport_input = driver.find_element(By.XPATH, '//*[@id="passportNoAll_0"]')
        passport_input.clear()
        passport_input.send_keys(passport_number)

        # Passport expiration
        Select(driver.find_element(By.XPATH, '//*[@id="passportDay_0"]')).select_by_value(f"{passport_exp_day:02d}")
        Select(driver.find_element(By.XPATH, '//*[@id="passportMonth_0"]')).select_by_value(f"{passport_exp_month:02d}")
        Select(driver.find_element(By.XPATH, '//*[@id="passportYear_0"]')).select_by_value(str(passport_exp_year))

        # Nationality selection (searchable dropdown)
        dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.searchable-select__selection'))
        )
        dropdown.click()

        search_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.searchable-select__search'))
        )
        search_input.clear()
        search_input.send_keys(natianalaty)

        option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'searchable-select__option') and text()='{natianalaty}']"))
        )
        option.click()
        print(f"Selected nationality: {natianalaty}")


        comfort_package = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'provider-package__select') and .//p[text()='Comfort']]"))
        )
        comfort_package.click()
        print("Selected 'Comfort' flight package")    

        time.sleep(7)
        print("finished")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
