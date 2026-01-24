#!/usr/bin/env python3
"""
Quick Test Runner
Simple script to run the test with different configurations.

Usage:
    python run_test.py              # Run locally with Chrome
    python run_test.py --firefox    # Run locally with Firefox
    python run_test.py --remote     # Run on BrowserStack with Chrome
    python run_test.py --remote --firefox   # Run on BrowserStack with Firefox
"""

import sys
import subprocess


def print_banner():
    """Print a nice banner"""
    print("\n" + "="*70)
    print("  AVIASALES FLIGHT BOOKING TEST - QUICK RUNNER")
    print("="*70 + "\n")


def print_usage():
    """Print usage instructions"""
    print("Usage:")
    print("  python run_test.py                    # Local Chrome")
    print("  python run_test.py --firefox          # Local Firefox")
    print("  python run_test.py --remote           # BrowserStack Chrome")
    print("  python run_test.py --remote --firefox # BrowserStack Firefox")
    print()


def run_test(use_remote=False, browser="Chrome"):
    """
    Run the test with specified configuration.
    
    Args:
        use_remote (bool): Whether to use BrowserStack
        browser (str): Browser name ("Chrome" or "Firefox")
    """
    print(f"Configuration:")
    print(f"  - Execution: {'BrowserStack (Remote)' if use_remote else 'Local'}")
    print(f"  - Browser: {browser}")
    print()
    
    # Modify the test file temporarily
    with open('test_flight_booking_with_excel.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update configuration
    content = content.replace(
        'USE_REMOTE_EXECUTION = False',
        f'USE_REMOTE_EXECUTION = {use_remote}'
    )
    content = content.replace(
        'SELECTED_BROWSER = "Chrome"',
        f'SELECTED_BROWSER = "{browser}"'
    )
    
    # Save modified file
    with open('test_flight_booking_with_excel.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Starting test execution...")
    print("-" * 70)
    
    # Run the test
    try:
        # Check if running in virtual environment
        venv_python = '/Users/meruyertbauyrzhanqyzy/sqat-testing/venv/bin/python'
        try:
            result = subprocess.run([venv_python, 'test_flight_booking_with_excel.py'])
        except FileNotFoundError:
            # Fallback to system python
            result = subprocess.run(['python3', 'test_flight_booking_with_excel.py'])
        
        return result.returncode == 0
        
    except KeyboardInterrupt:
        print("\n\n⚠ Test interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Error running test: {e}")
        return False


def main():
    """Main function"""
    print_banner()
    
    # Parse command line arguments
    args = sys.argv[1:]
    
    if '--help' in args or '-h' in args:
        print_usage()
        return
    
    # Determine configuration
    use_remote = '--remote' in args or '-r' in args
    use_firefox = '--firefox' in args or '-f' in args
    
    browser = "Firefox" if use_firefox else "Chrome"
    
    # Run the test
    success = run_test(use_remote=use_remote, browser=browser)
    
    # Print result
    print("\n" + "="*70)
    if success:
        print("✓ TEST EXECUTION COMPLETED")
    else:
        print("✗ TEST EXECUTION FAILED")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
