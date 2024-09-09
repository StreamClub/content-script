import os
import sys
import psycopg2
import psycopg2.extras
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
    GMR = 'group_movie_recommendation'
    GSR = 'group_series_recommendation'

def insert_rows(rows, type, conn, cur):
    query = f"INSERT INTO {type} (id, recommendations) VALUES %s ON CONFLICT (id) DO UPDATE SET recommendations = EXCLUDED.recommendations"
    values = [(int(row['id']), row['recommendations']) for row in rows]
    psycopg2.extras.execute_values(cur, query, values)
    conn.commit()

def upload_recommendations(type, conn, cur, batch_size=1000):
    with open(f'{type}.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter=',')
        print(f"Started uploading {type}...")

        batch = []
        for idx, row in enumerate(reader, start=1):
            batch.append(row)
            if idx % batch_size == 0:
                print(f"Processing batch ending with index: {idx}...")
                try:
                    insert_rows(batch, type, conn, cur)
                    batch = []
                except Exception as error:
                    print(f"Failed for batch ending with id: {row['id']}, because: {error}. Rollback...")
                    conn.rollback()

        # Insert remaining rows
        if batch:
            print(f"Processing the last batch ending with index: {idx}...")
            try:
                insert_rows(batch, type, conn, cur)
            except Exception as error:
                print(f"Failed for the last batch because: {error}. Rollback...")
                conn.rollback()

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
        print(sys.argv[1])
        print("Use: python3 upload_recos_to_rdb.py (MMR|SSR|UMR|USR|GMR|GSR)")
        sys.exit(1)
    
    type = Type[sys.argv[1]].value
    connect_and_upload(type)
