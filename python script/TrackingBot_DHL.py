import requests
from requests import RequestException
import smtplib
from email.mime.text import MIMEText
import time as mytime
from datetime import datetime
import pytz
from email.mime.multipart import MIMEMultipart
import configparser

# Read API credentials and email information from config file
config = configparser.ConfigParser()
config.read('/dhl_details.txt')

# DHL API credentials
api_key = config.get('DHL', 'API_KEY')
api_secret = config.get('DHL', 'API_SECRET')
tracking_number = config.get('DHL', 'TRACKING_NUMBER')

# Email credentials
sender_email = config.get('Email', 'SENDER_EMAIL')
sender_password = config.get('Email', 'SENDER_PASSWORD')
receiver_email = config.get('Email', 'RECIPIENT_EMAIL')

# DHL API endpoint with tracking number
url = f"https://api-eu.dhl.com/track/shipments?trackingNumber={tracking_number}"

# Initial status to check for updates
initial_status = ""

# Function to send an email with the package status
def send_email(status):
    # Configure the time zone to Peruvian time
    peru_timezone = pytz.timezone('America/Lima')
    current_time = datetime.now(peru_timezone).strftime("%B - %d - %Y\n%I:%M %p")

    # Create the HTML content for the email, including styles and structure
    html_content = f"""
        <html>
        <head>
            <style>
                body {{
                    background-color: #ffffff;
                    font-family: Arial, sans-serif;
                    color: #333333;
                }}
                .container {{
                    margin: 0 auto;
                    max-width: 600px;
                    padding: 20px;
                }}
                .logo {{
                    text-align: center;
                }}
                .logo img {{
                    max-width: 150px;
                }}
                .content {{
                    background-color: #ffffff;
                    padding: 20px;
                    margin-top: 20px;
                }}
                .update-title {{
                    font-weight: bold;
                    font-size: 18px;
                    color: #333333;
                    margin-bottom: 10px;
                }}
                .update-time {{
                    color: #666666;
                    margin-bottom: 20px;
                }}
                .update-location {{
                    font-weight: bold;
                    margin-bottom: 5px;
                }}
                .update-description {{
                    margin-bottom: 10px;
                }}
                .latest-update {{
                    background-color: #f1f1f1;
                    padding: 10px;
                    border-radius: 5px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="logo">
                    <img src="https://www.dhl.com/content/dam/dhl/global/core/images/logos/dhl-logo.svg" alt="DHL Logo">
                </div>
                <div class="content">
                    <div class="update-title">Tracking Number: {tracking_number}</div>
    """

    # Highlight the latest update as the most recent status
    if status:
        latest_update = status[0]
        location = latest_update["location"]["address"]["addressLocality"]
        description = latest_update["description"]
        html_content += f"""
            <div class="update-time latest-update" style="text-align: left;">
                <div><strong>NOW</strong></div>
                <div>{current_time}</div>
                <div class="update-location">{location}</div>
                <div class="update-description">{description}</div>
            </div>
        """

    # Iterate through remaining updates to add them to the email
    for i, s in enumerate(status[1:]):
        location = s["location"]["address"]["addressLocality"]
        description = s["description"]
        html_content += f"""
            <div class="update-location">{location}</div>
            <div class="update-description">{description}</div>
            <br>  <!-- Additional space between updates -->
        """
    # Finalize the HTML content
    html_content += """
                </div>
            </div>
        </body>
        </html>
    """

    # Configure the email message with MIME standards
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "New Update for DHL Package"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    # Attach HTML content to the email
    msg.attach(MIMEText(html_content, "html"))

    # Send the email using SMTP
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

# List to store past updates for reference
past_updates = []

# Main loop to check for updates every 15 minutes
while True:
    try:
        # Make API request
        headers = {"DHL-API-Key": api_key, "DHL-API-Secret": api_secret}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for non-2xx status codes

        # Parse response for status and shipment updates
        status = response.json()["shipments"][0]["status"]["description"]
        updates = response.json()["shipments"][0]["events"]

        # Check if status has changed
        if status != initial_status:
            # Update initial status
            initial_status = status

            # Clear past updates list
            past_updates.clear()

            # Add updates to past updates list
            for update in updates:
                date = update.get("date", "")
                time = update.get("time", "")
                location = update.get("location", "")
                description = update.get("description", "")
                update_info = {
                    "date": date,
                    "time": time,
                    "location": location,
                    "description": description
                }
                past_updates.append(update_info)

            # Send email with past updates
            send_email(past_updates)

            # End the script if the package is delivered
            if status == "Delivered":
                break

    except (RequestException, ValueError) as e:
        # Handle connection errors or JSON decoding errors
        print(f"An error occurred: {e}")
        # Wait for 1 minute before retrying the connection
        mytime.sleep(60)  # 60 seconds
        continue

    # Wait for 10 minutes before checking again
    mytime.sleep(600)  