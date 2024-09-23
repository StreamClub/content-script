import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
UAPI_TOKEN = os.getenv("UAPI_TOKEN")
UAPI_BASE_URL = os.getenv("UAPI_BASE_URL")
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT"))

def getAllGroups(page):
  url = f"{UAPI_BASE_URL}groups/all?pageNumber={page}"
  
  headers = {
      "accept": "application/json",
      "Authorization": f"Bearer {UAPI_TOKEN}"
  }
  response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
  data = json.loads(response.text)

  resultsArray = data['results']
  totalPages = data['totalPages']
  pageFound = (page <= totalPages)

  return resultsArray, pageFound 
