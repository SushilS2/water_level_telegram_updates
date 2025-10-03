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
    #logger.info("Token not available!")
    #raise

TOKEN = os.environ["TOKEN"] #'8278717297:AAH3aRu97RCab9zMF_oXkso_fKzEU9RnUP4'
CHAT_ID = '-4836215106'
API_KEY = ''

# Define the API endpoint URL
waltr_api_url = "https://api.waltr.in/v0/location/2548/tank"  # Example public API

headers = {
    "Authorization": "TOKEN dd5d65cb5c9d74403448d696560c6330b8b8ec68"
}

if __name__ == "__main__":
    logger.info(f"Token value: {SOME_SECRET}")
    try:
        #while True:
        # Send a GET request to the API
        response = requests.get(waltr_api_url, headers=headers)

        if response.status_code == 200:
                            
            # Check for HTTP errors (e.g., 404 Not Found, 500 Internal Server Error)
            response.raise_for_status()

            # If the request was successful, parse the JSON response
            data = response.json()
            domestic  = data["name"]["Domestic"]["current_water_level"]["water_level_in_percentage"]
            flush  = data["name"]["flush"]["current_water_level"]["water_level_in_percentage"]
            message = f"Domestic: {domestic}%, Flush: {flush}%"
            logger.info(f'Currect Water level: {message}')
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
            requests.post(url)
            #time.sleep(3600)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected error occurred: {req_err}")