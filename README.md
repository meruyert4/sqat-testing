# SQAT Testing

## Prerequisites
- Python 3.x

## Setup

1. Create virtual environment:
```bash
python -m venv venv
```

2. Activate virtual environment:
```bash
source venv/bin/activate
```

3. Install required packages:
```bash
pip install selenium webdriver-manager python-dotenv
```

4. Create .env with variables shown in .env.example

## Run Tests
```bash
python test_search.py
python test_login_logout.py
python test_flight_booking.py
```