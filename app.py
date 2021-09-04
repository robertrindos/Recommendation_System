from flask import Flask
import pandas as pd
import numpy as np
from google.cloud import storage

movies = pd.read_csv('gs://data_bucket_rr1/rotten_tomatoes_movies.csv')
print(movies.head(5))
titles = movies['movie_title']
output_info = movies[['movie_title', 'tomatometer_rating', 'directors', 'actors']]
chosen_movie = 'zootopia'

sim_matrix = pd.read_csv('gs://data_bucket_rr1/sim_matrix.csv')

# Function 1 - Searches 'chosen_movie' from the movie database
# returns the similarity scores for every movie in relation to 'chosen_movie'
# Cleans titles to account for incorrect capitalization and spaces
def get_sim_scores(chosen_movie, titles, cosine_sim):
    title = chosen_movie.replace(' ', '').lower()
    titles_clean = titles.apply(lambda x: str(x).replace(' ', '').lower())
    titles_clean = pd.Index(titles_clean)
    idx = titles_clean.get_loc(title)
    sim_list = list(enumerate(cosine_sim[idx]))
    return sim_list

# Function 2 - Sorts the similarity scores in descending order
# Returns the top 5 similarity scores (not including chosen_movie, it always has perfect score)
# Output_info describes what info will be provided from the top 5 similar movies
def top_5_list(sim_list, output_info):
    sim_list = sorted(sim_list, key=lambda x: x[1], reverse=True)
    top_5 = sim_list[0:6]
    top_5_indices = [i[0] for i in top_5]
    output = output_info.fillna(' ', inplace=False)
    return output.iloc[top_5_indices].reset_index(drop=True)


app = Flask(__name__)
@app.route("/")
def Home():
    return ("Home Page")