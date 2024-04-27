import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
capi_token = os.getenv("CAPI_TOKEN")

def get_page(userId, page):
  url = f"https://capi-xf6o.onrender.com/seenContent/{userId}?page={page}&pageSize=10"
  headers = {
      "accept": "application/json",
      "Authorization": f"Bearer {capi_token}"
  }
  response = requests.get(url, headers=headers, timeout=(5,5))
  data = json.loads(response.text)
  print(data)
  return data['results'], data['totalPages']
