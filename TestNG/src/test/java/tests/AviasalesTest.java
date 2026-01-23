package tests;

import base.BaseTest;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.Select;
import org.testng.Assert;
import org.testng.SkipException;
import org.testng.annotations.Test;
import java.util.List;
import java.util.Set;

/**
 * Aviasales Flight Booking Test Class
 * Demonstrates TestNG annotations, Log4j logging, and Extent Reports with screenshots
 */
public class AviasalesTest extends BaseTest {
    
    private static final String AVIASALES_URL = "https://www.aviasales.kz";
    private static final String DEPARTURE_CITY = "Астана";
    private static final String DESTINATION_CITY = "Уральск";
    
    /**
     * Complete flight booking test
     * Demonstrates: TestNG @Test annotation, logging, and full booking flow
     */
    @Test(priority = 1, description = "Complete flight booking from search to passenger details")
    public void testFlightBooking() {
        logger.info("Test started: Complete flight booking");
        
        // Step 1: Open Aviasales website
        logStep("Opening Aviasales website: " + AVIASALES_URL);
        driver.get(AVIASALES_URL);
        logPass("Website opened successfully");
        
        // Step 2: Handle Booking.com checkbox
        handleBookingCheckbox();
        
        // Step 3: Fill search form
        fillSearchForm();
        
        // Step 4: Select date
        selectFlightDate();
        
        // Step 5: Click search button
        clickSearchButton();
        
        // Step 6: Wait for search results and click first ticket
        clickFirstTicket();
        
        // Step 7: Click buy button
        clickBuyButton();
        
        // Step 8: Fill booking form
        fillBookingForm();
        
        logPass("Flight booking test completed successfully");
        logger.info("Test completed successfully");
    }
    
    /**
     * Handle Booking.com checkbox
     */
    private void handleBookingCheckbox() {
        logStep("Handling Booking.com checkbox");
        
        try {
            Thread.sleep(2000);
            WebElement bookingLabel = driver.findElement(By.xpath("//label[contains(., 'Booking.com')]"));
            
            WebElement checkboxInput = bookingLabel.findElement(By.tagName("input"));
            
            if (checkboxInput.isSelected()) {
                ((JavascriptExecutor) driver).executeScript("arguments[0].click();", bookingLabel);
                logStep("Booking.com checkbox was checked - unchecked it");
            } else {
                ((JavascriptExecutor) driver).executeScript("arguments[0].click();", bookingLabel);
                logStep("Clicked on Booking.com checkbox");
            }
            
            logPass("Booking.com checkbox handled successfully");
        } catch (Exception e) {
            logWarning("Failed to handle Booking.com checkbox: " + e.getMessage());
        }
    }
    
    /**
     * Fill search form with departure and destination cities
     */
    private void fillSearchForm() {
        logStep("Filling search form");
        
        try {
            Thread.sleep(1000);
            
            // Fill departure city
            WebElement fromInput = driver.findElement(By.xpath("//*[@id='avia_form_origin-input']"));
            fromInput.clear();
            fromInput.sendKeys(DEPARTURE_CITY);
            logStep("Entered departure city: " + DEPARTURE_CITY);
            
            Thread.sleep(1000);
            
            // Fill destination city
            WebElement toInput = driver.findElement(By.xpath("//*[@id='avia_form_destination-input']"));
            toInput.clear();
            toInput.sendKeys(DESTINATION_CITY);
            logStep("Entered destination city: " + DESTINATION_CITY);
            
            Thread.sleep(1000);
            
            logPass("Search form filled successfully");
        } catch (Exception e) {
            logger.error("Failed to fill search form: " + e.getMessage());
            Assert.fail("Failed to fill search form: " + e.getMessage());
        }
    }
    
    /**
     * Select flight date from calendar
     */
    private void selectFlightDate() {
        logStep("Selecting flight date");
        
        try {
            Thread.sleep(1000);
            
            // Click date picker button
            WebElement datePickerButton = driver.findElement(
                By.xpath("/html/body/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/form/div[1]/div[3]/div[1]/div[1]/button[1]")
            );
            datePickerButton.click();
            logStep("Date picker opened");
            
            Thread.sleep(2000);
            
            // Select target date
            WebElement targetDate = driver.findElement(
                By.cssSelector("div.s__vY0Kp_7_YUAgIkqP:nth-child(3) > table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(5) > td:nth-child(3) > div:nth-child(1) > button:nth-child(1) > div:nth-child(2)")
            );
            targetDate.click();
            logStep("Date selected: 28.02.2025");
            
            Thread.sleep(1000);
            
            // Confirm date selection
            try {
                WebElement confirmBtn = driver.findElement(
                    By.xpath("//button[contains(., 'Выбрать')] | //button[contains(., 'Готово')] | /html/body/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/form/div[1]/div[3]/div[1]/div[2]/div[1]/div/div/div/div/button")
                );
                confirmBtn.click();
                logStep("Date confirmed");
            } catch (Exception e) {
                logStep("No confirm button needed or already confirmed");
            }
            
            Thread.sleep(1000);
            
            logPass("Flight date selected successfully");
        } catch (Exception e) {
            logger.error("Failed to select date: " + e.getMessage());
            Assert.fail("Failed to select date: " + e.getMessage());
        }
    }
    
    /**
     * Click search button to find flights
     */
    private void clickSearchButton() {
        logStep("Clicking search button");
        
        try {
            WebElement searchButton = driver.findElement(By.cssSelector("button[data-test-id='form-submit']"));
            
            ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView({block: 'center'});", searchButton);
            Thread.sleep(1000);
            
            ((JavascriptExecutor) driver).executeScript("arguments[0].click();", searchButton);
            logStep("Search button clicked");
            
            // Wait for page to start loading results
            Thread.sleep(5000);
            
            logPass("Search initiated successfully");
        } catch (Exception e) {
            logWarning("Failed to click search button, trying fallback method");
            try {
                WebElement toInput = driver.findElement(By.xpath("//*[@id='avia_form_destination-input']"));
                toInput.sendKeys(Keys.ENTER);
                Thread.sleep(5000);
                logStep("Used Enter key on destination field as fallback");
            } catch (Exception ex) {
                logger.error("Failed to initiate search: " + ex.getMessage());
                Assert.fail("Failed to initiate search: " + ex.getMessage());
            }
        }
    }
    
    /**
     * Wait for search results and click first ticket
     */
    private void clickFirstTicket() {
        logStep("Waiting for search results");
        
        try {
            String currentUrl = driver.getCurrentUrl();
            logStep("Current URL: " + currentUrl);
            
            logStep("Searching for flights...");
            
            // Wait for results to load
            Thread.sleep(10000);
            
            WebElement ticketPrice = driver.findElement(By.cssSelector("div[data-test-id='price']"));
            
            ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView({block: 'center'});", ticketPrice);
            Thread.sleep(1000);
            
            ((JavascriptExecutor) driver).executeScript("arguments[0].click();", ticketPrice);
            logStep("Successfully clicked on the first ticket price");
            logPass("First ticket selected successfully");
        } catch (Exception e) {
            logger.error("Failed to click on ticket: " + e.getMessage());
            logStep("Final URL before fail: " + driver.getCurrentUrl());
            Assert.fail("Failed to click on ticket: " + e.getMessage());
        }
    }
    
    /**
     * Click buy button for Wingie proposal
     */
    private void clickBuyButton() {
        logStep("Looking for Wingie proposal");
        
        try {
            Thread.sleep(3000);
            
            // Check if Wingie exists
            List<WebElement> wingieElements = driver.findElements(By.xpath("//div[contains(text(), 'Wingie')]"));
            
            if (wingieElements.isEmpty()) {
                logWarning("Wingie proposal not found - skipping test");
                throw new SkipException("Wingie proposal not available in search results");
            }
            
            logStep("Wingie proposal found, clicking buy button");
            
            // Find the Buy button associated with Wingie
            // Based on HTML structure: data-test-id="text" contains Wingie, button is in parent/sibling
            WebElement buyButton = driver.findElement(
                By.xpath("//div[@data-test-id='text' and contains(text(), 'Wingie')]/ancestor::div[@data-test-id='proposal-0' or contains(@class, 'proposal')]//button")
            );
            
            String originalWindow = driver.getWindowHandle();
            
            ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView({block: 'center'});", buyButton);
            Thread.sleep(1000);
            
            ((JavascriptExecutor) driver).executeScript("arguments[0].click();", buyButton);
            logStep("Clicked 'Buy' button for Wingie proposal");
            
            // Wait for new window
            Thread.sleep(3000);
            
            Set<String> windowHandles = driver.getWindowHandles();
            for (String windowHandle : windowHandles) {
                if (!windowHandle.equals(originalWindow)) {
                    driver.switchTo().window(windowHandle);
                    break;
                }
            }
            
            logStep("Switched to new window: " + driver.getTitle());
            logPass("Buy button clicked for Wingie and switched to booking page");
        } catch (SkipException e) {
            throw e;
        } catch (Exception e) {
            logger.error("Failed to click buy button for Wingie: " + e.getMessage());
            logStep("Current URL: " + driver.getCurrentUrl());
            Assert.fail("Failed to click buy button for Wingie: " + e.getMessage());
        }
    }
    
    /**
     * Fill booking form with passenger details
     */
    private void fillBookingForm() {
        logStep("Filling booking form with passenger details");
        
        try {
            Thread.sleep(3000);
            
            // Booking data
            String email = "23232323@astanait.edu.kz";
            String phone = "7787296919";
            String name = "Meruyert";
            String lastname = "Boranbay";
            String passportNumber = "123456798";
            String nationality = "Казахстан";
            
            // Fill email
            WebElement emailInput = driver.findElement(By.xpath("//*[@id='contact_email']"));
            emailInput.clear();
            emailInput.sendKeys(email);
            logStep("Email entered: " + email);
            
            Thread.sleep(500);
            
            // Fill phone
            WebElement phoneInput = driver.findElement(By.xpath("//*[@id='contact_cellphone']"));
            phoneInput.clear();
            phoneInput.sendKeys(phone);
            logStep("Phone entered: " + phone);
            
            Thread.sleep(500);
            
            // Fill name
            WebElement nameInput = driver.findElement(By.xpath("//*[@id='firstName_0']"));
            nameInput.clear();
            nameInput.sendKeys(name);
            logStep("Name entered: " + name);
            
            Thread.sleep(500);
            
            // Fill lastname
            WebElement lastnameInput = driver.findElement(By.xpath("//*[@id='lastName_0']"));
            lastnameInput.clear();
            lastnameInput.sendKeys(lastname);
            logStep("Lastname entered: " + lastname);
            
            Thread.sleep(500);
            
            // Select gender (female)
            try {
                WebElement femaleLabel = driver.findElement(By.xpath("//*[@id='gender_F_0']"));
                if (!femaleLabel.isSelected()) {
                    femaleLabel.click();
                    logStep("Gender selected: Female");
                }
            } catch (Exception e) {
                logStep("Gender selection skipped or not needed");
            }
            
            Thread.sleep(500);
            
            // Fill date of birth
            Select daySelect = new Select(driver.findElement(By.xpath("//*[@id='birthDateDay_0']")));
            daySelect.selectByValue("02");
            
            Select monthSelect = new Select(driver.findElement(By.xpath("//*[@id='birthDateMonth_0']")));
            monthSelect.selectByValue("07");
            
            Select yearSelect = new Select(driver.findElement(By.xpath("//*[@id='birthDateYear_0']")));
            yearSelect.selectByValue("2005");
            logStep("Date of birth entered: 02/07/2005");
            
            Thread.sleep(500);
            
            // Fill passport number
            WebElement passportInput = driver.findElement(By.xpath("//*[@id='passportNoAll_0']"));
            passportInput.clear();
            passportInput.sendKeys(passportNumber);
            logStep("Passport number entered: " + passportNumber);
            
            Thread.sleep(500);
            
            // Fill passport expiration
            Select passportDay = new Select(driver.findElement(By.xpath("//*[@id='passportDay_0']")));
            passportDay.selectByValue("12");
            
            Select passportMonth = new Select(driver.findElement(By.xpath("//*[@id='passportMonth_0']")));
            passportMonth.selectByValue("12");
            
            Select passportYear = new Select(driver.findElement(By.xpath("//*[@id='passportYear_0']")));
            passportYear.selectByValue("2030");
            logStep("Passport expiration entered: 12/12/2030");
            
            Thread.sleep(500);
            
            // Select nationality
            WebElement dropdown = driver.findElement(By.cssSelector(".searchable-select__selection"));
            dropdown.click();
            
            Thread.sleep(1000);
            
            WebElement searchInput = driver.findElement(By.cssSelector(".searchable-select__search"));
            searchInput.clear();
            searchInput.sendKeys(nationality);
            
            Thread.sleep(1000);
            
            WebElement option = driver.findElement(
                By.xpath("//div[contains(@class, 'searchable-select__option') and text()='" + nationality + "']")
            );
            option.click();
            logStep("Nationality selected: " + nationality);
            
            Thread.sleep(1000);
            
            // Select comfort package
            WebElement comfortPackage = driver.findElement(
                By.xpath("//div[contains(@class, 'provider-package__select') and .//p[text()='Comfort']]")
            );
            comfortPackage.click();
            logStep("Selected 'Comfort' flight package");
            
            Thread.sleep(7000);
            
            logPass("Booking form filled successfully");
            logger.info("Finished filling booking form");
        } catch (Exception e) {
            logger.error("Failed to fill booking form: " + e.getMessage());
            Assert.fail("Failed to fill booking form: " + e.getMessage());
        }
    }
}
