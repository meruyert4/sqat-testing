# BDD Testing with Behave

This directory contains Behavior Driven Development (BDD) tests for the Aviasales flight booking and Reddit login/logout functionality.

## Structure

```
BDDTesting/
├── features/
│   ├── flight_booking.feature       # Feature file for flight booking scenarios
│   ├── login_logout.feature         # Feature file for login/logout scenarios
│   ├── environment.py               # Browser setup and teardown
│   └── steps/
│       ├── flight_booking_steps.py  # Step definitions for flight booking
│       └── login_logout_steps.py    # Step definitions for login/logout
└── README.md
```

## Requirements

Install the required packages:

```bash
pip install behave selenium webdriver-manager python-dotenv
```

## Environment Variables

Create a `.env` file in the root directory with your Reddit credentials:

```
USERNAME=your_reddit_username
PASSWORD=your_reddit_password
```

## Features

### 1. Flight Booking (3 scenarios)
- Search for available flights
- Select and proceed with flight booking
- Complete passenger information form

### 2. Login/Logout (2 scenarios)
- Successful login to Reddit
- Successful logout from Reddit

## Running Tests

### Run all tests:
```bash
cd BDDTesting
behave
```

### Run specific feature:
```bash
behave features/flight_booking.feature
behave features/login_logout.feature
```

### Run with verbose output:
```bash
behave -v
```

### Run specific scenario by name:
```bash
behave -n "Successful login to Reddit"
```

## Test Reports

Behave generates console output by default. For HTML reports, you can use:

```bash
behave --format html --outfile reports/report.html
```

## Notes

- Tests use Chrome browser (ensure Chrome is installed)
- ChromeDriver is automatically managed by webdriver-manager
- Each scenario runs independently with fresh browser instance
- Flight booking tests interact with aviasales.kz
- Login/logout tests require valid Reddit credentials in .env file
