import pandas as pd
from normalizing_functions import *
from api_calls import *
import os
import sys
import csv

def get_movies(start_date, end_date):
    (df, pages) = get_page(1, start_date, end_date)
    header = not os.path.exists('movies.csv')
    for page in range(2, pages):
        if (page % 20 == 0):
            df = format_dataset(df)
            df.to_csv('movies.csv', index=False, mode='a', header=header)
            header = False
            print(f"Processing: {int((page / pages) * 100)}%")
            try:
                (df, _) = get_page(page, start_date, end_date)
            except:
                print(f"WRITTEN UNTILL {int((page / pages) * 100)}%")
                log_execution(start_date, end_date, False, page-1)
                return -1
        else:
            try:
                (aux, _) = get_page(page, start_date, end_date)
            except:
                print(f"WRITTEN UNTILL {int((page / pages) * 100)}%")
                log_execution(start_date, end_date, False, page-1)
                return -1
            df = pd.concat([df, aux], ignore_index=True)
    return 0

def format_dataset(df):
    df = df.loc[:,['id', 'genre_ids', 'vote_average', 'release_date']]
    df['release_date'] = df['release_date'].apply(lambda x: normalize_date(x, df['release_date'].max()))
    df['vote_average'] = df['vote_average'].apply(normalize_vote)
    return pivot_genres(df)

def log_execution(start_date, end_date, success, page_number = 0):
    csv_filename = "executions.csv"
    header = ["Start Date", "End Date", "Date", "Success", "Page Number"]
    if success:
        data = [[start_date, end_date, time.time(), "True", page_number]]
    else:
        data = [[start_date, end_date, time.time(), "True", page_number]]
    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if(not os.path.exists('movies.csv')):
            writer.writerow(header)
        writer.writerows(data)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 script.py start_date end_date")
        sys.exit(1)
    start_date = sys.argv[1]
    end_date = sys.argv[2]
    start_time = time.time()
    res = get_movies(start_date, end_date)
    if res == 0:
        end_time = time.time()
        execution_time_seconds = end_time - start_time
        execution_time_minutes = int(execution_time_seconds // 60)
        execution_time_seconds = int(execution_time_seconds % 60)
        log_execution(start_date, end_date, start_time)

print(f'DONE: {execution_time_minutes}:{execution_time_seconds}s')
