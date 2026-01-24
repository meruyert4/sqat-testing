SUPPORTED_BROWSERS = {
    'windows': ['chrome', 'firefox'],
    'macos': ['chrome', 'firefox', 'safari']
}

OS_VERSIONS = {
    'windows': '11',
    'macos': 'Sonoma'
}

OS_NAMES = {
    'windows': 'Windows',
    'macos': 'OS X'
}

def validate_browser_os_combination(browser, os_type):
    """Validate if browser is supported on the given OS"""
    browser_lower = browser.lower()
    os_lower = os_type.lower()
    
    if os_lower not in SUPPORTED_BROWSERS:
        raise ValueError(f"Unsupported OS: {os_type}. Options: windows, macos")
    
    if browser_lower not in SUPPORTED_BROWSERS[os_lower]:
        raise ValueError(
            f"Browser '{browser}' not supported on {os_type}. "
            f"Available browsers for {os_type}: {', '.join(SUPPORTED_BROWSERS[os_lower])}"
        )
    
    return True

def get_os_config(os_type):
    """Get OS name and version for BrowserStack"""
    os_lower = os_type.lower()
    return {
        'os': OS_NAMES.get(os_lower, 'Windows'),
        'osVersion': OS_VERSIONS.get(os_lower, '11')
    }
