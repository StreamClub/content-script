import sys
from api_calls import get_user_seen
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def find_n_closest_to_user(df, user, n=5):
    matrix = df.drop(['id'], axis=1).values
    similarities = cosine_similarity([user], matrix)[0]
    similar_indices = similarities.argsort()
    closest_indices = similar_indices[-(n+1):-1]
    closest_ids = df.iloc[closest_indices]['id']
    closest_distances = similarities[closest_indices]
    result_df = pd.DataFrame({'id': closest_ids.values, 'distance': closest_distances})
    result_df = result_df.sort_values(by='distance', ascending=False)
    return result_df['id'].values

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 users_script.py user_id n_recomendations")
        sys.exit(1)
    user_id = sys.argv[1]
    n = int(sys.argv[2])
    (movies_ids, _) = get_user_seen(user_id)
    df = pd.read_csv("./movies.csv")
    filtered_df = df[df['id'].isin(movies_ids)]
    user_array = filtered_df.drop(['id'], axis=1).sum().values
    user_array = [x / 3 for x in user_array]
    recomendations = find_n_closest_to_user(df[~df['id'].isin(movies_ids)], user_array, n)
    print(recomendations)