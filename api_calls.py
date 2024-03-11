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
    url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=es-ES&page={page}&release_date.gte={start_date}&release_date.lte={end_date}&sort_by=popularity.desc&with_runtime.gte={min_runtime}&with_watch_monetization_types={monetization_types}&watch_region={watch_region}"
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

def get_movie_details(id):
    url = f"https://api.themoviedb.org/3/movie/{id}?language=en-US"
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

def get_user_seen(user_id):
    url = f"https://capi-xf6o.onrender.com/seenContent/movies/{user_id}?page=1&pageSize=10"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + os.getenv("CAPI_TOKEN")
    }
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    if "error" in data:
        raise Exception(data["error"])
    return [movie["movieId"] for movie in data["results"]], data['totalPages']

def get_genres():
    url = "https://api.themoviedb.org/3/genre/movie/list?language=es"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + os.getenv("TMDB_API_KEY")
    }
    response = requests.get(url, headers=headers, timeout=(5,5))
    data = json.loads(response.text)
    return [genre["id"] for genre in data["genres"]]