def get_release_year(x):
  return int(x.split('-')[0])

def normalize_vote(x):
  if isinstance(x, (int, float)):
    return x/10
  else:
    return 0

def normalize_date(x, max):
  if isinstance(x, (int, float)):
    return x/max
  else:
    return 0
  
def pivot_genres(df):
    unique_genre_ids = set()
    for genre_ids in df['genre_ids']:
        unique_genre_ids.update(genre_ids)

    # Create binary columns for each genre ID
    for genre_id in unique_genre_ids:
        df[genre_id] = df['genre_ids'].apply(lambda x: 1 if genre_id in x else 0)

    # Drop the original 'genre_ids' column
    df.drop('genre_ids', axis=1, inplace=True)
    return df