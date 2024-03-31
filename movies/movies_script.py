import pandas as pd
from movies import get_movie_details_for_id
from api_calls import *
import os
import sys
import csv

def get_movies(start_date, end_date):
    (ids, pages) = get_page(1, start_date, end_date)
    header = not os.path.exists('movies.csv')
    print(f"TOTAL PAGES: {pages}")
    df = get_movie_details_for_id(ids)
    for page in range(2, pages + 1):
        try:
            (ids, _) = get_page(page, start_date, end_date)
            aux = get_movie_details_for_id(ids)
        except:
            print(f"WRITTEN UNTIL {int((page / pages) * 100)}%")
            log_execution(start_date, end_date, False, page-1)
            return -1
        df = pd.concat([df, aux], ignore_index=True)
        if (page % 5 == 0):
            df.to_csv('movies.csv', index=False, mode='a', header=header)
            df = pd.DataFrame()
            header = False
            print(f"Processing: {int((page / pages) * 100)}%")
    df.to_csv('movies.csv', index=False, mode='a', header=header)
    return 0

def log_execution(start_date, end_date, success, page_number = 0):
    csv_filename = "executions.csv"
    header = ["Start Date", "End Date", "Date", "Success", "Page Number"]
    if success:
        data = [[start_date, end_date, time.time(), "True", page_number]]
    else:
        data = [[start_date, end_date, time.time(), "True", page_number]]
    exists = os.path.exists('executions.csv')
    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if(not exists):
            writer.writerow(header)
        writer.writerows(data)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 movies_script.py start_date end_date")
        sys.exit(1)
    start_date = sys.argv[1]
    end_date = sys.argv[2]
    start_time = time.time()
    print("START PROCESSING...")
    res = get_movies(start_date, end_date)
    if res == 0:
        end_time = time.time()
        execution_time_seconds = end_time - start_time
        execution_time_minutes = int(execution_time_seconds // 60)
        execution_time_seconds = int(execution_time_seconds % 60)
        log_execution(start_date, end_date, start_time)

print(f'DONE: {execution_time_minutes}:{execution_time_seconds}s')
