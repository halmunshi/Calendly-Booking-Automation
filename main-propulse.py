import asyncio
import logging
from flask import Flask, request, jsonify
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from datetime import datetime

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def convert_iso(iso_date):
    """
    Convert ISO 8601 date to 'Day, Month Day' and 12-hour time format.
    Example: '2024-10-25T13:30:00Z' -> ('Friday, October 25', '1:30pm')
    """
    try:
        # Parse the ISO date string into a datetime object
        dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
        time_slot = dt.strftime("%I:%M%p").lstrip("0").lower()

        return dt, time_slot
    except ValueError as e:
        logger.error(f"Invalid ISO date format: {e}")
        return None, None


async def book_appointment(name, email, phone, details, date, time_slot):
    """Automate the Calendly booking using Playwright."""

    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(
                headless=False)  # Use headless=True for production
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto('https://calendly.com/hasan-processpulse/30min')
            await page.wait_for_load_state("networkidle")

            # Navigate to the next month if needed
            today = datetime.today()
            while date.year > today.year or (date.year == today.year
                                             and date.month > today.month):
                logger.info("Navigating to the next month...")
                await page.get_by_label("Go to next month").click()
                if today.month == 12:
                    today = today.replace(month=1, year=today.year + 1)
                else:
                    today = today.replace(month=today.month + 1)

            # Select the provided date dynamically
            formatted_date = date.strftime("%A, %B %-d")
            logger.info(f"Selecting date: {formatted_date}")
            await page.get_by_label(f"{formatted_date} - Times").click()

            # Select the provided time slot dynamically
            logger.info(f"Selecting time: {time_slot}")
            await page.get_by_role("button", name=f"{time_slot}").click()
            logger.info("Time selected successfully.")
            await page.get_by_label(f"Next {time_slot}").click()
            logger.info("Clicked Next.")
            # Wait for the form to load completely
            await page.wait_for_load_state("networkidle")

            # Fill in the booking form dynamically
            logger.info("Filling in the booking form...")
            await page.get_by_label("Name *").click()
            await page.get_by_label("Name *").fill(name)
            await page.get_by_label("Email *").click()
            await page.get_by_label("Email *").fill(email)
            await page.get_by_label("Is there any process in").click()
            await page.get_by_label("Is there any process in").fill(phone)

            # Click the "Schedule Event" button
            await page.get_by_role("button", name="Schedule Event").click()
            await asyncio.sleep(5)  # Non-blocking wait

            logger.info("Appointment booked successfully!")
            return "success"

        except PlaywrightTimeoutError as e:
            logger.error(f"Timeout error: {e}")
            return "timeout"
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return "error"
        finally:
            await browser.close()


@app.route('/book', methods=['POST'])
def handle_request():
    """Handle incoming HTTP requests with dynamic booking details."""
    data = request.json

    # Extract variables from the HTTP request
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    details = data.get('details')
    iso_date = data.get('date')  # ISO 8601 format

    # Convert ISO date to readable date and time
    date, time_slot = convert_iso(iso_date)

    # Validate that all required data is present
    if not all([name, email, phone, details, date, time_slot]):
        logger.error("Invalid request. Missing required data.")
        return jsonify(
            {"message":
             "Invalid request. Please provide all required data."}), 400

    # Run the Playwright automation with the provided data
    result = asyncio.run(
        book_appointment(name, email, phone, details, date, time_slot))

    if result == "success":
        return jsonify({"message": "Appointment booked successfully!"}), 200
    elif result == "timeout":
        return jsonify(
            {"message": "Failed to book appointment due to timeout."}), 500
    else:
        return jsonify({"message": "An unexpected error occurred."}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
