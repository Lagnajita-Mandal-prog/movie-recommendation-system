import pandas as pd
import numpy as np
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load datasets
movies = pd.read_csv("tmdb_5000_movies.csv.zip")
credits = pd.read_csv("tmdb_5000_credits.csv.zip")

# Merge on title
movies = movies.merge(credits, on='title')

# Select useful columns
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

# Drop rows with missing values
movies.dropna(inplace=True)

# Function to convert JSON strings to Python lists
def convert(text):
    try:
        return [i['name'] for i in ast.literal_eval(text)]
    except:
        return []

# Apply transformations
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(lambda x: [i['name'] for i in ast.literal_eval(x)[:3]] if pd.notnull(x) else [])
movies['crew'] = movies['crew'].apply(lambda x: [i['name'] for i in ast.literal_eval(x) if i['job'] == 'Director'] if pd.notnull(x) else [])

# Fill missing overviews with empty string to avoid errors
movies['overview'] = movies['overview'].apply(lambda x: x if isinstance(x, str) else "")

# Combine all text features into 'tags'
movies['tags'] = movies['overview'].apply(lambda x: x.split()) + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

# Create new DataFrame
new_df = movies[['movie_id', 'title', 'tags']].copy()

# Convert list to string
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))

# Convert to lowercase
new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())

# Vectorization
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()

# Similarity matrix
similarity = cosine_similarity(vectors)

# Recommender function
def recommend(movie):
    movie = movie.lower()
    if movie not in new_df['title'].str.lower().values:
        return ["Movie not found :("]
    index = new_df[new_df['title'].str.lower() == movie].index[0]
    distances = list(enumerate(similarity[index]))
    distances = sorted(distances, reverse=True, key=lambda x: x[1])
    recommended_movies = [new_df.iloc[i[0]].title for i in distances[1:6]]
    return recommended_movies
