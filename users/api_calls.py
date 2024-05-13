import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
CAPI_TOKEN = os.getenv("CAPI_TOKEN")
CAPI_BASE_URL = os.getenv("CAPI_BASE_URL")
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT"))

def getSeenContentPage(page):
  url = f"{CAPI_BASE_URL}seenContent/?page={page}"
  
  headers = {
      "accept": "application/json",
      "Authorization": f"Bearer {CAPI_TOKEN}"
  }
  response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
  data = json.loads(response.text)

  resultsArray = data['results']
  userId = None
  moviesIds = []
  seriesIds = []
  pageFound = resultsArray.__len__() != 0

  if pageFound:
    results = resultsArray[0]
    userId = results['userId']
    moviesIds = results['movies']
    seriesIds = results['series']
    pageFound = True

  return userId, moviesIds, seriesIds, pageFound
