# How to Run the Project

## Prerequisites
```bash
java -version  # Java 11+
mvn -version   # Maven 3.6+
```

Install if needed:
- **Java**: `brew install openjdk@11` (macOS)
- **Maven**: `brew install maven` (macOS)
- **Chrome**: Ensure installed

## Run Tests

### Command Line
```bash
cd TestNG
mvn clean test
```

### IntelliJ IDEA
1. Open `TestNG` folder
2. Right-click `testng.xml` → Run
3. Or right-click `AviasalesTest.java` → Run

### Eclipse
1. Import → Maven → Existing Maven Projects
2. Right-click `testng.xml` → Run As → TestNG Suite

## View Results

### Extent Report
```bash
open test-output/ExtentReport.html
```

### Log Files
```bash
cat test-output/logs/automation.log
```

### Screenshots (on failure)
```
test-output/screenshots/{testName}_{timestamp}.png
```

## Project Features

### 1. TestNG Annotations (30 points)
- `@BeforeClass` - Setup Extent Reports
- `@BeforeMethod` - Initialize WebDriver
- `@Test` - Test methods with priority and description
- `@AfterMethod` - Capture screenshots, close browser
- `@AfterClass` - Flush reports

### 2. Log4j Logging (30 points)
- Configured in `src/test/resources/log4j2.xml`
- Logs test start, steps, errors, completion
- Output to console and file: `test-output/logs/automation.log`

### 3. Extent Reports & Screenshots (40 points)
- HTML report: `test-output/ExtentReport.html`
- Screenshots captured on test failure
- Screenshots attached to Extent Report
- Detailed test execution timeline

## Troubleshooting

```bash
# Maven not found
brew install maven

# Java not found  
brew install openjdk@11

# ChromeDriver issues
# WebDriverManager handles automatically

# View logs
tail -f test-output/logs/automation.log
```
