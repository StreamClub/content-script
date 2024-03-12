import pandas as pd
from api_calls import get_movie_details

def get_movie_details_for_id(ids):
  details = []
  for id in ids:
    details.append(get_movie_details(id))
  df = pd.DataFrame(details)
  return df