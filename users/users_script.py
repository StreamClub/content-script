import json
import time
import pandas as pd
import sys
from api_calls import getSeenContentPage

def get_updated_DataFrame(dfSeenContent, userId, moviesIds, seriesIds):
  dfMovies = pd.DataFrame( { 'contentId': moviesIds }, dtype=int )
  dfMovies['userId'] = userId
  dfMovies['category'] = 'movie'

  dfSeries = pd.DataFrame( { 'contentId': seriesIds }, dtype=int )
  dfSeries['userId'] = userId
  dfSeries['category'] = 'series'

  dfSeenContent = pd.concat([dfSeenContent, dfMovies, dfSeries], ignore_index=True)
  return dfSeenContent

def get_users():
  dfSeenContent = pd.DataFrame()
  page = 1
  
  userId, moviesIds, seriesIds, pageFound = getSeenContentPage(page)
  while (pageFound):
    print(f'Procesando página {page}...')
    dfSeenContent = get_updated_DataFrame(dfSeenContent, userId, moviesIds, seriesIds)
    page += 1
    userId, moviesIds, seriesIds, pageFound = getSeenContentPage(page)

  dfSeenContent.to_csv(f'users.csv', index=False, mode='w', header=True)

#---------------------------------------------#
def execute_and_time(callback):
  start_time = time.time()
  print("Procesando...")
  callback()
  end_time = time.time()
  execution_time_seconds = end_time - start_time
  execution_time_minutes = int(execution_time_seconds // 60)
  execution_time_seconds = int(execution_time_seconds % 60)
  print(f'Procesamiento finalizado en {execution_time_minutes}:{execution_time_seconds}s')

if __name__ == "__main__":
  if len(sys.argv) != 1:
    print("Uso: python users_script.py")
    sys.exit(1)
  execute_and_time(get_users)
  
