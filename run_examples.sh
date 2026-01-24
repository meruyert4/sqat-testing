echo "Running test examples with different configurations..."
echo "========================================="

# BrowserStack Tests (Default)
echo "BROWSERSTACK TESTS:"
echo "========================================="

# Chrome on Windows
echo "1. Chrome on Windows (BrowserStack):"
python test_flight_booking_with_excel.py --browser chrome --os windows

# Firefox on Windows
echo "2. Firefox on Windows (BrowserStack):"
python test_flight_booking_with_excel.py --browser firefox --os windows

# Safari on macOS
echo "3. Safari on macOS (BrowserStack):"
python test_flight_booking_with_excel.py --browser safari --os macos

# Local Tests
echo ""
echo "LOCAL TESTS:"
echo "========================================="

# Chrome locally
echo "4. Chrome on Windows (Local):"
python test_flight_booking_with_excel.py --local --browser chrome --os windows

# Firefox locally
echo "5. Firefox on macOS (Local):"
python test_flight_booking_with_excel.py --local --browser firefox --os macos

# Custom Excel file
echo ""
echo "CUSTOM CONFIGURATION:"
echo "========================================="
echo "6. With custom Excel file:"
python test_flight_booking_with_excel.py --browser chrome --os windows --excel my_test_data.xlsx
