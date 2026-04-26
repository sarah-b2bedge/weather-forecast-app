import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

def get_data(place, forecast_days):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={place}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()
    # Get data for the specified number of days (8 entries per day)
    filtered_data = data['list'][:forecast_days * 8]
    return filtered_data

# Only executes when this file is run directly, not when imported as a module
if __name__ == "__main__":
    data = get_data("aaa", 1)
    print(data)