import os
import sys
import psycopg2
import csv
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get the connection string from the environment variable
connection_string = os.getenv('DATABASE_URL')

# Connect to the Postgres database
conn = psycopg2.connect(connection_string)

# Create a cursor object
cur = conn.cursor()

# Execute SQL commands to retrieve the current time and version from PostgreSQL
def upload_recommendations(type):
  with open(f'{type}_recommendations.csv', 'r') as file:
    reader = csv.DictReader(file, delimiter=',')
    print(f"Started uploading {type}...")
    for idx, row in enumerate(reader, start=1):
      try:
        id = int(row['Id'])
        recommendations = row['recommendations']
        query = f"INSERT INTO {type}_{type}_recommendation (Id, recommendations) VALUES ({id}, '{recommendations}')"
        cur.execute(query)
        conn.commit()
      except Exception as error:
        print(f"Failed for id: {row['Id']}, because: {error}.\n Rollback...")
        conn.rollback()
      if(idx%100 == 0):
        print(f"Progress.... on line {idx}")

if __name__ == "__main__":
  if len(sys.argv) != 2:
      print("Uso: python3 upload_recommendations.py (movie or series)")
      sys.exit(1)
  type = sys.argv[1]
  upload_recommendations(type)
  print("Done processing, closing connections...")
  # Close the cursor and connection
  cur.close()
  conn.close()
  print("Done!")
