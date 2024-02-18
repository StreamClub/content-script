import sys
from api_calls import get_user_seen
import pandas as pd

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 users_script.py user_id")
        sys.exit(1)
    user_id = sys.argv[1]
    (movies_ids, _) = get_user_seen(user_id)
    df = pd.read_csv("./movies.csv")
    filtered_df = df[df['id'].isin(movies_ids)]
    print(filtered_df.head())