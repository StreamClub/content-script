import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
CAPI_TOKEN = os.getenv("CAPI_TOKEN")
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT"))

def getSeenContentPage(page):
  # TODO: Cuando se disponga del endpoint cambiar por la nueva url
  url = f"https://capi-xf6o.onrender.com/seenContent/{page}?page={1}&pageSize=10"
  #################################
  
  headers = {
      "accept": "application/json",
      "Authorization": f"Bearer {CAPI_TOKEN}"
  }
  response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
  data = json.loads(response.text)

  return data['results'], data['results'] != []
