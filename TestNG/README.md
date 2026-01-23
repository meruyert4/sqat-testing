# Aviasales Selenium Automation Project

## How to Run

### Prerequisites
```bash
java -version  # Java 11+
mvn -version   # Maven 3.6+
```

### Run Tests
```bash
cd TestNG
mvn clean test
```

### View Report
```bash
open test-output/ExtentReport.html
```

---

## Project Details

### Technologies
- Java 11, Selenium 4.16.1, TestNG 7.8.0
- WebDriverManager 5.6.3, Extent Reports 5.1.1, Log4j2 2.22.0

### Structure
```
TestNG/
├── src/test/java/
│   ├── base/BaseTest.java
│   └── tests/AviasalesTest.java
├── pom.xml
└── testng.xml
```

### Installation
```bash
mvn -version
```

### 3. Navigate to Project Directory
```bash
cd TestNG
```

### 4. Install Dependencies
```bash
mvn clean install -DskipTests
```

## Running the Tests

### Option 1: Using Maven Command Line
```bash
mvn clean test
```

### Option 2: Using TestNG XML Directly
```bash
mvn test -DsuiteXmlFile=testng.xml
```

### Option 3: Using IDE (IntelliJ IDEA / Eclipse)
1. Import the project as a Maven project
2. Right-click on `testng.xml` → Run
3. Or right-click on `AviasalesTest.java` → Run as TestNG Test

## Test Execution Flow

The `AviasalesTest` performs the following steps:

1. **Opens Aviasales website** (`https://www.aviasales.kz`)
2. **Handles Booking.com checkbox** (unchecks if selected)
3. **Fills departure city** (Астана)
4. **Fills destination city** (Уральск)
5. **Clicks search button** to initiate flight search
6. **Waits for search results** page to load
7. **Clicks on first ticket price** to view details

## Features Implemented

### BaseTest Class
✅ **WebDriver Management**
- Automatic ChromeDriver setup using WebDriverManager
- Configurable implicit and explicit waits
- Chrome options for maximized window and disabled notifications

✅ **Extent Reports Integration**
- Professional HTML reports with test execution details
- System information (OS, Browser, Environment)
- Test step logging
- Screenshot attachment on test failure

✅ **Log4j2 Logging**
- Console and file appenders
- Timestamped log files with rolling file policy
- Debug level logging for detailed troubleshooting
- Separate loggers for test and base packages

✅ **Screenshot Capture**
- Automatic screenshot on test failure
- Timestamped screenshot filenames
- Screenshots attached to Extent Report

### AviasalesTest Class
✅ **Clean Code Principles**
- Separated methods for each action
- Clear method names describing functionality
- Reusable locators as constants
- Comprehensive logging for each step

✅ **Stable Waits**
- No `Thread.sleep()` used
- `WebDriverWait` with `ExpectedConditions`
- Element visibility and clickability checks
- URL change detection for page transitions

✅ **Robust Element Interactions**
- JavaScript clicks for stubborn elements
- Scroll into view before clicking
- Fallback strategies (e.g., Enter key press)
- Exception handling with meaningful error messages

## Reports and Logs

### Extent Report
- **Location**: `test-output/ExtentReport.html`
- **Contains**: Test execution timeline, pass/fail status, screenshots, step logs
- Open in any web browser after test execution

### Log Files
- **Location**: `test-output/logs/automation.log`
- **Contains**: Detailed execution logs with timestamps
- Rolling file policy creates dated backups

### Screenshots
- **Location**: `test-output/screenshots/`
- **Naming**: `{testName}_{timestamp}.png`
- Automatically captured on test failure

## Configuration

### Timeouts (BaseTest.java)
```java
private static final int IMPLICIT_WAIT_TIMEOUT = 10;  // seconds
private static final int EXPLICIT_WAIT_TIMEOUT = 20;  // seconds
```

### Browser Options (BaseTest.java)
```java
options.addArguments("--start-maximized");
options.addArguments("--disable-blink-features=AutomationControlled");
options.addArguments("--disable-notifications");
```

### Log Levels (log4j2.xml)
- **Root Logger**: INFO level
- **Test Package**: DEBUG level
- **Base Package**: DEBUG level

## TestNG Annotations Used

```java
@BeforeClass  - Initialize Extent Reports (once per class)
@BeforeMethod - Setup WebDriver (before each test method)
@Test         - Test method execution
@AfterMethod  - Teardown, screenshot capture, quit browser
@AfterClass   - Flush Extent Reports
```

## Troubleshooting

### ChromeDriver Issues
If you encounter ChromeDriver compatibility issues:
- Ensure Chrome browser is up to date
- WebDriverManager automatically handles driver versions
- Check logs for WebDriverManager errors

### Element Not Found
- Increase explicit wait timeout in `BaseTest.java`
- Check if website structure has changed
- Review locators in `AviasalesTest.java`

### Test Failures
- Check `test-output/ExtentReport.html` for detailed failure information
- Review screenshots in `test-output/screenshots/`
- Check logs in `test-output/logs/automation.log`

## Best Practices Followed

✅ Page Object Model (POM) can be easily implemented
✅ DRY principle (Don't Repeat Yourself)
✅ Single Responsibility Principle
✅ Meaningful variable and method names
✅ Comprehensive logging and reporting
✅ No hardcoded waits (`Thread.sleep`)
✅ Proper exception handling
✅ Clean code structure

## Maven Commands Cheat Sheet

```bash
# Clean and compile
mvn clean compile

# Run tests
mvn test

# Run specific test class
mvn test -Dtest=AviasalesTest

# Run with different TestNG suite
mvn test -DsuiteXmlFile=testng.xml

# Skip tests during install
mvn install -DskipTests

# Generate test reports
mvn surefire-report:report
```

## Assignment Submission Checklist

✅ Complete Maven project structure
✅ All dependencies properly configured in `pom.xml`
✅ TestNG annotations correctly used
✅ Log4j2 with console and file appenders
✅ Extent Reports with screenshots
✅ Clean, readable, and well-documented code
✅ No `Thread.sleep()` - only stable waits
✅ BaseTest class with reusable setup/teardown
✅ Working test case based on Python implementation
✅ Professional HTML report generation

## Author
Software Quality Assurance and Testing Course Project  
Astana IT University

## License
Educational Project - 2026
