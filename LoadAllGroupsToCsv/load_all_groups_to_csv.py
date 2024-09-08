import time
import pandas as pd
import sys
from api.api_calls import getAllGroups

def get_updated_DataFrame(dfGroups, newGroups):
  for group in newGroups:
    group.pop('name', None)
  print(newGroups)
  dfNewGroups = pd.DataFrame( newGroups )
  dfGroups = pd.concat([dfGroups, dfNewGroups], ignore_index=True)
  return dfGroups

def get_groups():
  dfGroups = pd.DataFrame()
  page = 1
  resultsArray, pageFound = getAllGroups(page)
  while (pageFound):
    print(f'Procesando página {page}...')
    dfGroups = get_updated_DataFrame(dfGroups, resultsArray)
    page += 1
    resultsArray, pageFound = getAllGroups(page)

  dfGroups.to_csv(f'groups.csv', index=False, mode='w', header=True)

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
    print("Uso: python load_all_groups_to_csv.py")
    sys.exit(1)
  execute_and_time(get_groups)