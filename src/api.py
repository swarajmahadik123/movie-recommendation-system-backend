import pickle
import pandas as pd
import os
from flask import Flask, jsonify, request  # type: ignore

# Define the base directory (the path to the project folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACTS_DIR = os.path.join(BASE_DIR, '../artifacts')

# Load the movie list and similarity matrix
new_df = pickle.load(open(os.path.join(ARTIFACTS_DIR, 'movie_list.pkl'), 'rb'))
similarity = pickle.load(open(os.path.join(ARTIFACTS_DIR, 'similarity.pkl'), 'rb'))

def recommend_movies(movie_title, num_recommendations=19):
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

    # Get the top N recommendations based on similarity
    recommended_movies = [
        (str(new_df.iloc[i[0]].title), int(new_df.iloc[i[0]].movie_id)) 
        for i in distance_array[1:num_recommendations + 1]
    ]
    
    # Insert the original movie at the start of the list
    original_movie = (str(new_df.iloc[movie_idx].title), int(new_df.iloc[movie_idx].movie_id))
    recommended_movies.insert(0, original_movie)  # Add original movie to the top
    
    return recommended_movies

app = Flask(__name__)

@app.route('/recommend', methods=['GET'])
def recommend():
    movie_title = request.args.get('title')
    recommendations = recommend_movies(movie_title)

    # If the recommendations contain an error message, return an error response
    if isinstance(recommendations, list) and recommendations[0] == "Movie not found!":
        return jsonify({"error": "Movie not found!"}), 404
    
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app
