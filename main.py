import logging
import logging.handlers
import requests
import time
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

TOKEN_WALTR = os.environ["TOKEN_WALTER"] 
TOKEN_TEL = os.environ["TOKEN_TEL"] 
TOKEN_NBS = os.environ["TOKEN_NBS"]
CHAT_ID = '-1003034311751' #'5167371789' 

# Define the API endpoint URL
waltr_api_url = "https://api.waltr.in/v0/location/2548/tank"  # Example public API

headers_waltr = {
    "Authorization": f"TOKEN {TOKEN_WALTR}" 
}

nbsense_api_url = "https://api.nbsense.in/water_ms/get_latest_data?meter_id=351"  # Example public API

headers_nbs = {
    "Authorization": f"Bearer {TOKEN_NBS}" 
}

if __name__ == "__main__":
    logger.info(f"Starting script")
    try:
        response_nbs = requests.get(nbsense_api_url, headers=headers_nbs)

        if response_nbs.status_code == 200:
            
            # Check for HTTP errors (e.g., 404 Not Found, 500 Internal Server Error)
            response_nbs.raise_for_status()

            # If the request was successful, parse the JSON response
            data_nbs = response_nbs.json()
            water_level_percent_nbs = float(data_nbs['today_flow'])
            water_level_percent_nbs =f"{(water_level_percent_nbs / 3) * 2:.2f}"
            logger.info(f"UGT Water Level: {water_level_percent_nbs} Kl")
            
            message_nbs = f"UGT Water Level:\n{water_level_percent_nbs} KL\n\n"

        # Send a GET request to the API
        response = requests.get(waltr_api_url, headers=headers_waltr)

        if response.status_code == 200:
                            
            # Check for HTTP errors (e.g., 404 Not Found, 500 Internal Server Error)
            response.raise_for_status()

            # If the request was successful, parse the JSON response
            data = response.json()
            message  = "\n".join(
                                    f"{tank['name']}: {tank['current_water_level']['water_level_in_percentage']}%"
                                    for tank in data
                                )
            water_level_percent_domastic = data[0]['current_water_level']['water_level_in_percentage']
            water_level_percent_flush = data[1]['current_water_level']['water_level_in_percentage']

            if (water_level_percent_domastic < 20):                
                message = f"""
**CRITICAL WATER ALERT**

The water level in the overhead tank is now at {water_level_percent_domastic:.1f}%.

Please start conserving water immediately. We are taking steps to restore the supply, but your responsible usage is crucial.

{message}

Thank you.
- Aspen Committee
"""
            elif (water_level_percent_flush < 20):
                message = f"""
**CRITICAL WATER ALERT**

The water level in the overhead tank is now at {water_level_percent_domastic:.1f}%.

Please start conserving water immediately. We are taking steps to restore the supply, but your responsible usage is crucial.

{message}

Thank you.
- Aspen Committee
"""
            else:
                message = f"Current water level of OHT:\n{message}"

            logger.info(f"Message sent to telegram: {message}")

            url = f"https://api.telegram.org/bot{TOKEN_TEL}/sendMessage?chat_id={CHAT_ID}&text={message_nbs + message}"
            requests.post(url)
            
            logger.info(f"ending script")

    except requests.exceptions.HTTPError as http_err:
        logger.info(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        logger.info(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        logger.info(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        logger.info(f"An unexpected error occurred: {req_err}")