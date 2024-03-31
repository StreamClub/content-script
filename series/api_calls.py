import requests
import json
import pandas as pd
import time
import os
from dotenv import load_dotenv

load_dotenv()
min_runtime = os.getenv("MIN_RUNTIME")
monetization_types = os.getenv("MONETIZATION_TYPES")
watch_region = os.getenv("WATCH_REGION")

def get_page(page, start_date, end_date):
    url = f"https://api.themoviedb.org/3/discover/tv?first_air_date.gte={start_date}&first_air_date.lte={end_date}&include_adult=false&include_null_first_air_dates=false&language=es-ES&page={page}&sort_by=popularity.desc&watch_region={watch_region}&with_watch_monetization_types={monetization_types}"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + os.getenv("TMDB_API_KEY")
    }
    while True:
        response = requests.get(url, headers=headers, timeout=(5,5))
        if response.status_code == 429:
            print("Rate limit exceeded. Waiting for 60 seconds before retrying...")
            time.sleep(60)  # Wait for a minute
            continue
        elif response.status_code == 200:
            data = json.loads(response.text)
            ids = [movie['id'] for movie in data['results']]
            return ids, data['total_pages']
        else:
            print(f"Error: {response.status_code}. Failed to fetch data.")
            return None, None

def get_series_details(id):
    url = f"https://api.themoviedb.org/3/tv/{id}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + os.getenv("TMDB_API_KEY")
    }
    while True:
        response = requests.get(url, headers=headers, timeout=(5,5))
        if response.status_code == 429:
            print("Rate limit exceeded. Waiting for 60 seconds before retrying...")
            time.sleep(60)  # Wait for a minute
            continue
        elif response.status_code == 200:
            return json.loads(response.text)
        else:
            print(f"Error: {response.status_code}. Failed to fetch data.")
            return None, None
