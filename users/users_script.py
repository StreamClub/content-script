import json
import time
import pandas as pd
import sys
from api_calls import get_page

def get_users(users_list):
  for user in users_list:
    content, total_pages = get_page(user, 1)
    df = pd.DataFrame(content)
    for page in range(2, total_pages + 1):
      content,_ = get_page(user, page)
      aux = pd.DataFrame(content)
      df = pd.concat([df, aux], ignore_index=True)
    df.to_csv(f'user_{user}.csv', index=False, mode='a', header=True)
  """ (ids, pages) = get_page(1, start_date, end_date)
  header = not os.path.exists('series.csv')
  print(f"TOTAL PAGES: {pages}")
  df = get_series_details_for_id(ids)
  for page in range(2, pages + 1):
      try:
          (ids, _) = get_page(page, start_date, end_date)
          aux = get_series_details_for_id(ids)
      except:
          print(f"WRITTEN UNTIL {int((page / pages) * 100)}%")
          log_execution(start_date, end_date, False, page-1)
          return -1
      df = pd.concat([df, aux], ignore_index=True)
      if (page % 5 == 0):
          df.to_csv('series.csv', index=False, mode='a', header=header)
          df = pd.DataFrame()
          header = False
          print(f"Processing: {int((page / pages) * 100)}%")
  df.to_csv('series.csv', index=False, mode='a', header=header)
  return 0 """

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("Uso: python3 users_script.py \"[userid1, userid2]\"")
    sys.exit(1)
  users_list = sys.argv[1]
  start_time = time.time()
  print("START PROCESSING...")
  res = get_users(json.loads(users_list))
  end_time = time.time()
  execution_time_seconds = end_time - start_time
  execution_time_minutes = int(execution_time_seconds // 60)
  execution_time_seconds = int(execution_time_seconds % 60)

print(f'DONE: {execution_time_minutes}:{execution_time_seconds}s')
