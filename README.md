# Calendly Automation Booking API

This application provides a simple Flask-based API to automate bookings on a specific Calendly page using Playwright. It's designed to handle the entire booking flow—from selecting a date and time to filling out the attendee information—automatically.

## Features
- **Automated Booking**: Uses Playwright to navigate the Calendly UI, select slots, and submit forms.
- **Dynamic Scheduling**: Supports booking for specific dates and times provided via API, including handling month navigation.
- **Robust Error Handling**: Provides clear feedback if a date/time is unavailable or if a timeout occurs.
- **JSON API**: Accepts booking details (name, email, phone, details, date) as JSON for easy integration with other services.

## Setup & Running

### Prerequisites
- Python 3.10+
- [Playwright](https://playwright.dev/python/docs/intro)

### 1. Install Dependencies
Using pip:
```bash
pip install flask playwright gunicorn
playwright install chromium
```

Or using Poetry:
```bash
poetry install
poetry run playwright install chromium
```

### 2. Run the App
```bash
python main.py
```
The server will start on port `8080`.

## API Usage

### Book an Appointment
- **Endpoint**: `POST /book`
- **Content-Type**: `application/json`

#### Request Payload
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "1234567890",
  "details": "I'd like to discuss the project.",
  "date": "2024-10-25T13:30:00Z"
}
```

#### Success Response (`200 OK`)
```json
{
  "message": "Appointment booked successfully!"
}
```

#### Error Responses
- `400 Bad Request`: Missing data or invalid JSON.
- `404 Not Found`: Date or time slot is unavailable on the Calendly page.
- `500 Internal Server Error`: Automation timeout or unexpected error.

## Project Structure
- `main.py`: Contains the Flask server and the `book_appointment` automation logic.
- `pyproject.toml`: Defines dependencies and tool configurations.
- `booking_confirmation.png`: (Optional) Example screenshot of a successful booking.

## Deployment on Replit
This project is configured for Replit. To host it:
1. Click the **Publish** button.
2. Select **Autoscale** for a web API.
3. Ensure the run command is set to `python main.py`.
