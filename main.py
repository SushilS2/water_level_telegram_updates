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

TOKEN = '8278717297:AAH3aRu97RCab9zMF_oXkso_fKzEU9RnUP4'
CHAT_ID = '-4836215106'
API_KEY = ''

# Define the API endpoint URL
waltr_api_url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&outputsize=full&apikey=demo"  # Example public API

if __name__ == "__main__":
    logger.info(f"Token value: {SOME_SECRET}")
    try:
        #while True:
        # Send a GET request to the API
        response = requests.get(waltr_api_url)

        if response.status_code == 200:
                            
            # Check for HTTP errors (e.g., 404 Not Found, 500 Internal Server Error)
            response.raise_for_status()

            # If the request was successful, parse the JSON response
            data = response.json()
            last_refreshed  = data["Meta Data"]["3. Last Refreshed"]
            message = data["Time Series (5min)"][last_refreshed]["1. open"]#'Current Domestic water level - 18 %\nCurrent Flush water level - 13 %\n'
            logger.info(f'Weather in Berlin: {message}')
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