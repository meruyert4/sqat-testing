# Test Configuration Guide

## Command Line Flags

Run tests with different browser and OS combinations using command line flags:

```bash
python test_flight_booking_with_excel.py --browser <BROWSER> --os <OS> --excel <EXCEL_FILE> [--local]
```

## Available Options

### Execution Mode
- `--use-browserstack` - Run on BrowserStack cloud (default: True)
- `--local` - Run tests locally on your machine (disables BrowserStack)

### Operating Systems
- `windows` - Windows 11 (supports Chrome, Firefox)
- `macos` - macOS Sonoma (supports Chrome, Firefox, Safari)

### Browsers
- `chrome` - Google Chrome (Windows, macOS)
- `firefox` - Mozilla Firefox (Windows, macOS)
- `safari` - Safari (macOS only)

### Excel File
- `--excel` - Path to Excel test data file (default: test_data.xlsx)

## Examples

### BrowserStack Tests (Default)
```bash
# Chrome on Windows (BrowserStack - default)
python test_flight_booking_with_excel.py --browser chrome --os windows

# Firefox on Windows (BrowserStack)
python test_flight_booking_with_excel.py --browser firefox --os windows

# Safari on macOS (BrowserStack)
python test_flight_booking_with_excel.py --browser safari --os macos
```

### Local Tests
```bash
# Chrome locally (bypasses BrowserStack)
python test_flight_booking_with_excel.py --local --browser chrome --os windows

# Firefox locally
python test_flight_booking_with_excel.py --local --browser firefox --os macos
```

### Windows Tests
```bash
# Chrome on Windows
python test_flight_booking_with_excel.py --browser chrome --os windows

# Firefox on Windows
python test_flight_booking_with_excel.py --browser firefox --os windows
```

### macOS Tests
```bash
# Chrome on macOS
python test_flight_booking_with_excel.py --browser chrome --os macos

# Firefox on macOS
python test_flight_booking_with_excel.py --browser firefox --os macos

# Safari on macOS (Safari only works on macOS)
python test_flight_booking_with_excel.py --browser safari --os macos
```

### Custom Excel File
```bash
python test_flight_booking_with_excel.py --browser chrome --os windows --excel my_data.xlsx
```

## Default Values
If no flags are provided:
- BrowserStack: True (runs on cloud)
- Browser: Chrome
- OS: Windows
- Excel: test_data.xlsx

Use `--local` flag to run tests on your local machine instead of BrowserStack.

## Browser/OS Compatibility

| Browser | Windows | macOS |
|---------|---------|-------|
| Chrome  | ✅      | ✅    |
| Firefox | ✅      | ✅    |
| Safari  | ❌      | ✅    |

## Configuration Files

- `test_config.py` - Browser/OS validation and configuration
- `test_flight_booking_with_excel.py` - Main test file with command line support
- `.env` - BrowserStack credentials (BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY)
- `test_data.xlsx` - Test data for flight booking

## Notes

- BrowserStack is enabled by default (use `--local` to run locally)
- All tests run on BrowserStack unless `--local` flag is provided
- Invalid browser/OS combinations will show an error message
- Safari can only run on macOS
- Local execution requires browsers to be installed on your machine
