import os
import sys
import psycopg2
import csv
from dotenv import load_dotenv
from enum import Enum

load_dotenv()
connection_string = os.getenv('DATABASE_URL')
class Type(Enum):
    MMR = 'movie_movie_recommendation'
    SSR = 'series_series_recommendation'
    UMR = 'user_movie_recommendation'
    USR = 'user_series_recommendation'

def insert_row(row, type, conn, cur):
    id = int(row['id'])
    recommendations = row['recommendations']
    print(recommendations)
    query = f"""
        INSERT INTO {type} (id, recommendations)
        VALUES ({id}, '{recommendations}')
        ON CONFLICT (id) DO UPDATE SET recommendations = '{recommendations}'
    """
    cur.execute(query)
    conn.commit()

def upload_recommendations(type, conn, cur):
  with open(f'{type}.csv', 'r') as file:
    reader = csv.DictReader(file, delimiter=',')
    print(f"Started uploading {type}...")
    for idx, row in enumerate(reader, start=1):
      try:
        insert_row(row, type, conn, cur)
      except Exception as error:
        print(f"Failed for id: {row['id']}, because: {error}.\n Rollback...")
        conn.rollback()
      if(idx%100 == 0):
        print(f"Progress.... on line {idx}")

def connect_and_upload(type):
    conn = psycopg2.connect(connection_string)
    cur = conn.cursor()

    try:
       upload_recommendations(type, conn, cur)
    except Exception as error:
      print(f"Failed to upload recommendations because: {error}")
    finally:
      print("Done processing, closing connections...")
      cur.close()
      conn.close()


if __name__ == "__main__":
  if len(sys.argv) != 2 or sys.argv[1] not in Type.__members__:
      print("Use: python3 upload_recommendations.py (MMR|SSR|UMR|USR)")
      sys.exit(1)
  
  type = Type[sys.argv[1]].value
  connect_and_upload(type)
  
  
  
  
  
  
