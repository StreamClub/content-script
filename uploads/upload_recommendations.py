import os
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
with open('uploads/recommendations.csv', 'r') as file:
  reader = csv.DictReader(file, delimiter=',')
  for row in reader:
    movie_id = int(row['Id'])
    recommendations = row['recommendations']
    query = f"INSERT INTO movie_movie_recommendation (Id, recommendations) VALUES ({movie_id}, '{recommendations}')"
    cur.execute(query)

# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
