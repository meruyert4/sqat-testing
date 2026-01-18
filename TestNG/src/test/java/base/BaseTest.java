package base;

import com.aventstack.extentreports.ExtentReports;
import com.aventstack.extentreports.ExtentTest;
import com.aventstack.extentreports.MediaEntityBuilder;
import com.aventstack.extentreports.reporter.ExtentSparkReporter;
import com.aventstack.extentreports.reporter.configuration.Theme;
import io.github.bonigarcia.wdm.WebDriverManager;
import org.apache.commons.io.FileUtils;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.ITestResult;
import org.testng.annotations.AfterClass;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.BeforeMethod;

import java.io.File;
import java.io.IOException;
import java.time.Duration;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * Base Test class providing common setup and teardown functionality
 * Implements WebDriver management, Extent Reports, and Log4j2 logging
 */
public class BaseTest {
    
    protected WebDriver driver;
    protected WebDriverWait wait;
    protected static ExtentReports extentReports;
    protected ExtentTest extentTest;
    protected static Logger logger = LogManager.getLogger(BaseTest.class);
    
    private static final int IMPLICIT_WAIT_TIMEOUT = 10;
    private static final int EXPLICIT_WAIT_TIMEOUT = 45;
    private static final String REPORTS_PATH = "test-output/ExtentReport.html";
    private static final String SCREENSHOTS_PATH = "test-output/screenshots/";
    
    /**
     * Initialize Extent Reports before all tests
     * Configures report theme, title, and document name
     */
    @BeforeClass
    public void setUpExtentReports() {
        if (extentReports == null) {
            ExtentSparkReporter sparkReporter = new ExtentSparkReporter(REPORTS_PATH);
            sparkReporter.config().setTheme(Theme.STANDARD);
            sparkReporter.config().setDocumentTitle("Aviasales Automation Test Report");
            sparkReporter.config().setReportName("Flight Booking Test Results");
            sparkReporter.config().setTimeStampFormat("yyyy-MM-dd HH:mm:ss");
            
            extentReports = new ExtentReports();
            extentReports.attachReporter(sparkReporter);
            extentReports.setSystemInfo("Application", "Aviasales.kz");
            extentReports.setSystemInfo("Browser", "Chrome");
            extentReports.setSystemInfo("Operating System", System.getProperty("os.name"));
            extentReports.setSystemInfo("Test Environment", "QA");
            
            logger.info("Extent Reports initialized successfully");
        }
    }
    
    /**
     * Set up WebDriver and browser configurations before each test method
     * Initializes ChromeDriver with WebDriverManager and configures waits
     */
    @BeforeMethod
    public void setUp(ITestResult result) {
        logger.info("=== Starting Test: {} ===", result.getMethod().getMethodName());
        
        // Create Extent Test for current test method
        extentTest = extentReports.createTest(result.getMethod().getMethodName());
        extentTest.info("Test execution started");
        
        // Setup WebDriverManager and ChromeDriver
        WebDriverManager.chromedriver().setup();
        logger.info("ChromeDriver setup completed using WebDriverManager");
        
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--start-maximized");
        options.addArguments("--disable-blink-features=AutomationControlled");
        options.addArguments("--disable-notifications");
        
        driver = new ChromeDriver(options);
        logger.info("ChromeDriver initialized with options");
        
        // Configure waits
        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(IMPLICIT_WAIT_TIMEOUT));
        wait = new WebDriverWait(driver, Duration.ofSeconds(EXPLICIT_WAIT_TIMEOUT));
        logger.info("WebDriver waits configured - Implicit: {}s, Explicit: {}s", 
                    IMPLICIT_WAIT_TIMEOUT, EXPLICIT_WAIT_TIMEOUT);
        
        extentTest.pass("WebDriver initialized successfully");
    }
    
    /**
     * Tear down after each test method
     * Captures screenshot on failure and closes browser
     */
    @AfterMethod
    public void tearDown(ITestResult result) {
        String testName = result.getMethod().getMethodName();
        
        if (result.getStatus() == ITestResult.FAILURE) {
            logger.error("Test FAILED: {}", testName);
            extentTest.fail("Test failed: " + result.getThrowable().getMessage());
            
            // Capture screenshot on failure
            String screenshotPath = captureScreenshot(testName);
            if (screenshotPath != null) {
                try {
                    extentTest.fail("Screenshot on failure", 
                        MediaEntityBuilder.createScreenCaptureFromPath(screenshotPath).build());
                    logger.info("Screenshot captured and attached to report");
                } catch (Exception e) {
                    logger.error("Failed to attach screenshot to report: {}", e.getMessage());
                }
            }
        } else if (result.getStatus() == ITestResult.SUCCESS) {
            logger.info("Test PASSED: {}", testName);
            extentTest.pass("Test completed successfully");
        } else if (result.getStatus() == ITestResult.SKIP) {
            logger.warn("Test SKIPPED: {}", testName);
            extentTest.skip("Test skipped: " + result.getThrowable());
        }
        
        // Quit browser
        if (driver != null) {
            driver.quit();
            logger.info("WebDriver closed");
        }
        
        logger.info("=== Test Completed: {} ===\n", testName);
    }
    
    /**
     * Flush Extent Reports after all tests
     */
    @AfterClass
    public void tearDownExtentReports() {
        if (extentReports != null) {
            extentReports.flush();
            logger.info("Extent Reports flushed successfully. Report location: {}", REPORTS_PATH);
        }
    }
    
    /**
     * Capture screenshot and save to file
     * 
     * @param testName Name of the test for screenshot file naming
     * @return Path to the saved screenshot
     */
    protected String captureScreenshot(String testName) {
        try {
            // Create screenshots directory if it doesn't exist
            File screenshotDir = new File(SCREENSHOTS_PATH);
            if (!screenshotDir.exists()) {
                screenshotDir.mkdirs();
            }
            
            // Generate timestamp for unique filename
            String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"));
            String fileName = testName + "_" + timestamp + ".png";
            String filePath = SCREENSHOTS_PATH + fileName;
            
            // Capture screenshot
            TakesScreenshot screenshot = (TakesScreenshot) driver;
            File sourceFile = screenshot.getScreenshotAs(OutputType.FILE);
            File destinationFile = new File(filePath);
            
            FileUtils.copyFile(sourceFile, destinationFile);
            logger.info("Screenshot captured: {}", filePath);
            
            return filePath;
        } catch (IOException e) {
            logger.error("Failed to capture screenshot: {}", e.getMessage());
            return null;
        }
    }
    
    /**
     * Log test step to both logger and Extent Report
     * 
     * @param message Step description
     */
    protected void logStep(String message) {
        logger.info(message);
        extentTest.info(message);
    }
    
    /**
     * Log test pass step to both logger and Extent Report
     * 
     * @param message Step description
     */
    protected void logPass(String message) {
        logger.info("PASS: {}", message);
        extentTest.pass(message);
    }
    
    /**
     * Log test warning to both logger and Extent Report
     * 
     * @param message Warning message
     */
    protected void logWarning(String message) {
        logger.warn(message);
        extentTest.warning(message);
    }
}
