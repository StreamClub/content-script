import pandas as pd
from api_calls import get_series_details

def get_series_details_for_id(ids):
  details = []
  for id in ids:
    details.append(get_series_details(id))
  df = pd.DataFrame(details)
  return df