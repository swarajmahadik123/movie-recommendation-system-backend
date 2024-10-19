import pickle
import pandas as pd
import os

# Define the base directory (the path to the project folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACTS_DIR = os.path.join(BASE_DIR, '../artifacts')

# Load the movie list and similarity matrix
new_df = pickle.load(open(os.path.join(ARTIFACTS_DIR, 'movie_list.pkl'), 'rb'))
similarity = pickle.load(open(os.path.join(ARTIFACTS_DIR, 'similarity.pkl'), 'rb'))

def recommend_movies(movie_title, num_recommendations=5):
    movie_title = movie_title.strip().lower()  # Trim and convert to lower case
    print(f"Searching for movie title: '{movie_title}'")
    
    # Check if the movie exists in the DataFrame
    if movie_title not in new_df['title'].str.lower().values:
        print("Movie not found!")
        return ["Movie not found!"]
    
    # Get the index of the movie
    movie_idx = new_df[new_df['title'].str.lower() == movie_title].index[0]

    # Get similarity scores for the selected movie
    distance_array = list(enumerate(similarity[movie_idx]))
    
    # Sort based on similarity scores (descending order)
    distance_array = sorted(distance_array, key=lambda x: x[1], reverse=True)

    # Debugging output to check distances
    print(f"Distances for {movie_title}: {[x[1] for x in distance_array[:10]]}")
    
    # Get the top N recommendations based on similarity
    recommended_movies = [
        (str(new_df.iloc[i[0]].title), int(new_df.iloc[i[0]].movie_id)) 
        for i in distance_array[1:num_recommendations + 1]
    ]
    
    return recommended_movies

    # Check if the movie exists in the DataFrame
    if movie_title not in new_df['title'].values:
        print("Movie not found!")
        return ["Movie not found!"]
    
    # Get the index of the movie
    movie_idx = new_df[new_df['title'] == movie_title].index[0]

    # Get similarity scores for the selected movie
    distance_array = list(enumerate(similarity[movie_idx]))
    
    # Sort based on similarity scores (descending order)
    distance_array = sorted(distance_array, key=lambda x: x[1], reverse=True)

    # Debugging output to check distances
    print(f"Distances for {movie_title}: {[x[1] for x in distance_array[:10]]}")
    
    # Get the top N recommendations based on similarity
    recommended_movies = [
        (str(new_df.iloc[i[0]].title), int(new_df.iloc[i[0]].movie_id)) 
        for i in distance_array[1:num_recommendations + 1]
    ]
    
    return recommended_movies