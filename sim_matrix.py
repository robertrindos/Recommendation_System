
# Importing Libraries
import pandas as pd
import numpy as np
import string
import re

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#from sklearn.preprocessing import StandardScaler, Normalizer

from google.cloud import storage
import os
from io import StringIO

# 1. Cleans text features
def clean_text_features(text):
    clean_features = text.fillna(' ', inplace=False)
    for col in clean_features:
        clean_features[col] = clean_features[col].apply(lambda x: str(x).replace(' ', ''))
        clean_features[col] = clean_features[col].apply(lambda x: str(x).replace(',', ' '))
        clean_features[col] = clean_features[col].apply(lambda x: str(x).lower())
        clean_features[col] = clean_features[col].apply(lambda x: str(x).replace('&', ''))
        clean_features[col] = clean_features[col].apply(lambda x: str(x).replace('.', ''))
    return clean_features


# 2. Creates a Bag-of-Words for each movie
def create_bow(clean_text, feature_list):
    bow_list = clean_text[feature_list].agg(' '.join, axis=1)
    # for loop removes duplicate words within each movie's BoW
    for bow in bow_list:
        re.sub(r'\b(.+)\s+\1\b', r'\1', str(bow_list))
    return bow_list


# 3. Creates a word-count matrix from the bag-of-words list
def count_vectorize(bow_list):
    count_vectorizer = CountVectorizer()
    count_vectorizer.fit(bow_list)
    count_transform = count_vectorizer.transform(bow_list)
    soup_count_array = count_transform.toarray()
    count_matrix = pd.DataFrame(soup_count_array)
    return count_matrix


# 4. Trims matrix to only include terms seen more than x amount of time (count_treshold)
def count_vect_trim(count_matrix, count_treshold):
    compact_matrix = count_matrix.loc[:, (count_matrix.sum(axis=0) > count_treshold)]
    return compact_matrix


# Applies the ratings to scale the similarity scores
# Work in Progress!!! Not Completed
# def apply_scalers(sim_list, ratings, scaler):
#    scaler.fit(ratings)
#    std_ratings = scaler.transform(ratings)
#    for idx in range(len(sim_list)):
#       sim_list[idx] = sim_list[idx] * (std_ratings[idx] / 10)
#    return sim_list



def main():
    #### Defining Variables ####
    print("Loading & Preprocessing Data...")

    # Defining GitHub URL to read .csv file
    url = 'https://raw.githubusercontent.com/robertrindos/Recommendation-System/main/rotten_tomatoes_movies.csv'
    movies = pd.read_csv(url)

    # Defining text features for Word-Count Matrix
    text_feature_list = ['genres', 'directors', 'authors', 'actors', 'production_company']
    text_features = movies[text_feature_list]

    # Defining movie titles
    titles = movies['movie_title']

    # Defining Ratings
    ratings = movies[['tomatometer_rating']]

    # Defining what info will be shown with recommendation output
    output_info = movies[['movie_title', 'tomatometer_rating', 'directors', 'actors']]

    # Defining movie to find recommendations for
    chosen_movie = 'zootopia'

    #### Functions Deployed ####

    # 1 - Text Cleaning
    clean_text = clean_text_features(text_features)

    # 2 - Creates Bag-of-Words
    bow_list = create_bow(clean_text, text_feature_list)

    print("Done!")
    print("Processing Text Data...")

    # 3 - Creates a Word-Count Matrix
    count_matrix = count_vectorize(bow_list)

    print("Done!")
    print("Trimming Data...")

    # 4 - Trims Matrix for Less Computations
    count_treshold = 10
    compact_matrix = count_vect_trim(count_matrix, count_treshold)

    print("Done!")
    print("Running Similarity Function (May Take A While)...")

    # 5 - Cosine Similarity
    cosine_sim = cosine_similarity(compact_matrix, compact_matrix)
    sim_matrix = pd.DataFrame(cosine_sim, index=cosine_sim.index())

    print("Done!")
    print("Converting to .csv and Uploading to Google Storage...")

    io = StringIO()
    cosine_sim.to_csv(io)
    io.seek(0)
    gcs.get_bucket('data_bucket_rr1').blob('sim_matrix.csv').upload_from_file(io, content_type='text/csv')

    print("Done! sim_matrix.csv Uploaded.")
    
    return titles, cosine_sim


if __name__ == "__main__":
    titles, cosine_sim = main()