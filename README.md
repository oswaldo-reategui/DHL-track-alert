# DHL Package Tracking Bot

## Introduction

This repository contains a Python script for a DHL Package Tracking Bot. The script automates tracking DHL shipments and notifies the user via email about status updates. It's designed to continuously check the shipment status and send real-time updates, making it an efficient tool for closely monitoring important deliveries.

## Features

- **Real-time Tracking:** Continuously checks for updates on the shipment status from the DHL API.
- **Email Notifications:** Sends detailed email notifications for every new update about the package's status.
- **Robust Error Handling:** Implements error handling for API request failures or data parsing issues.
- **Configurable:** Easily customizable for different tracking numbers and user credentials through a configuration file.

## Technologies

- Python
- Requests library for API calls
- SMTP for sending emails
- Python's standard libraries: `datetime`, `time`, `configparser`

## Setup and Configuration

### 1. Clone the repository:
`
git clone https://github.com/your-github-username/DHL-Package-Tracking-Bot.git
`
### 2. Install the required dependencies:
`
pip install requests pytz
`
### 3. Configuration:
Edit the `dhl_details.txt` file with the appropriate DHL API credentials, tracking number, and email details.

## Usage

Run the script using Python:
`
python TrackingBot_DHL.py
`
The script will start tracking the package and send email updates on status changes.

## Code Overview

### Main Functionalities
- **API Communication:** Interacts with DHL's tracking API to retrieve shipment status.
- **Email Alert System:** Composes and sends HTML formatted emails with the latest tracking information.
- **Continuous Monitoring:** Runs in a loop, periodically checking for updates.

### Error Handling
Implements try-except blocks to handle potential issues during API requests and data processing.

### Timezone Handling
Utilizes pytz to work with timezones, ensuring accurate time stamps in the emails based on the Peruvian timezone.

## Contribution

Suggestions and contributions are welcome. Please feel free to fork the repository and submit pull requests.

## Contact

For collaboration or queries, feel free to connect with me on [LinkedIn](https://www.linkedin.com/in/oswaldo-reategui/) or reach me at [Outlook](mailto:oswaldo_reategui@outlook.com).

## License

This project is licensed under the MIT License.
