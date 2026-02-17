# Calendly Automation Booking API

This application provides a simple Flask-based API to automate bookings on a specific Calendly page using Playwright.

## Features
- **Automated Booking**: Uses Playwright to navigate Calendly and fill out booking forms.
- **Dynamic Scheduling**: Supports booking for specific dates and times provided via API.
- **JSON API**: Accepts booking details (name, email, phone, details, date) as JSON.

## Setup & Running
1. **Install Dependencies**:
   ```bash
   pip install flask playwright gunicorn
   playwright install chromium
   ```
2. **Run the App**:
   ```bash
   python main.py
   ```
   The server will start on port `8080` (or `5000` if configured for Replit).

## API Usage
- **Endpoint**: `POST /book`
- **Payload Example**:
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "details": "I'd like to discuss the project.",
    "date": "2024-10-25T13:30:00Z"
  }
  ```

## Development
- `main.py`: The main entry point for the Flask application and Playwright logic.
- `pyproject.toml`: Dependency management via Poetry.
