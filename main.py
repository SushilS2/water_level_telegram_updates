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

try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "Token not available!"
    
TOKEN = os.environ["TOKEN"] 
CHAT_ID = '-1003034311751'

# Define the API endpoint URL
waltr_api_url = "https://api.waltr.in/v0/location/2548/tank"  # Example public API

headers = {
    "Authorization": f"{SOME_SECRET}" 
}

if __name__ == "__main__":
    logger.info(f"Starting script")
    try:
        #while True:
        # Send a GET request to the API
        response = requests.get(waltr_api_url, headers=headers)

        if response.status_code == 200:
                            
            # Check for HTTP errors (e.g., 404 Not Found, 500 Internal Server Error)
            response.raise_for_status()

            # If the request was successful, parse the JSON response
            data = response.json()
            message  = "\n".join(
                                    f"{tank['name']}: {tank['current_water_level']['water_level_in_percentage']}%"
                                    for tank in data
                                )
            message = f"Current water level of OHT:\n{message}"

            logger.info(f"Message sent to telegram: {message}")

            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
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