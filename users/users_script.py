import json
import time
import pandas as pd
import sys
from api_calls import getSeenContentPage


def get_users():
  dfSeenContent = pd.DataFrame()
  
  # TODO: Cuando se disponga del endpoint cambiar el valor de page a 1
  # page = 1
  #################################
  page = 21
  
  jsonContent, pageFound = getSeenContentPage(page)
  while (pageFound):
    print(f'Página {page}...')
    dfNewSeenContent = pd.DataFrame(jsonContent)
    
    # TODO: Cuando se disponga del endpoint eliminar esta línea
    dfNewSeenContent['userId'] = page
    #################################

    dfSeenContent = pd.concat([dfSeenContent, dfNewSeenContent], ignore_index=True)
    page += 1
    jsonContent, pageFound = getSeenContentPage(page)

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
  
