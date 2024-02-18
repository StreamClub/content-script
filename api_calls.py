import requests
import json
import pandas as pd
import time
import os
from dotenv import load_dotenv

load_dotenv()
min_vote = '10'
min_runtime = '10'

headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + os.getenv("API_KEY")
    }

def get_page(page, start_date, end_date):
    url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=es-ES&page={page}&release_date.gte={start_date}&release_date.lte={end_date}&sort_by=popularity.desc&vote_count.gte={min_vote}&with_runtime.gte={min_runtime}"
    while True:
        response = requests.get(url, headers=headers, timeout=(5,5))
        if response.status_code == 429:
            print("Rate limit exceeded. Waiting for 60 seconds before retrying...")
            time.sleep(60)  # Wait for a minute
            continue
        elif response.status_code == 200:
            data = json.loads(response.text)
            return pd.json_normalize(data['results']), data['total_pages']
        else:
            print(f"Error: {response.status_code}. Failed to fetch data.")
            return None, None