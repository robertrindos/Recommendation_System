
# Importing Libraries
import pandas as pd
import numpy as np
import string
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler, Normalizer


# Cleans text features
def clean_text_features(text):
    clean_features = text.fillna(' ', inplace=False)
    for col in clean_features:
        clean_features[col] = clean_features[col].apply(lambda x: str(x).replace(' ', ''))
        clean_features[col] = clean_features[col].apply(lambda x: str(x).replace(',', ' '))
        clean_features[col] = clean_features[col].apply(lambda x: str(x).lower())
        clean_features[col] = clean_features[col].apply(lambda x: str(x).replace('&', ''))
        clean_features[col] = clean_features[col].apply(lambda x: str(x).replace('.', ''))
    return clean_features


# creates a Bag-of-Words for each movie
def create_bow(clean_text, feature_list):
    bow_list = clean_text[feature_list].agg(' '.join, axis=1)
    # for loop removes duplicate words within each movie's BoW
    for bow in bow_list:
        re.sub(r'\b(.+)\s+\1\b', r'\1', str(bow_list))
    return bow_list


# Creates a word-count matrix from the bag-of-words list
def count_vectorize(bow_list):
    count_vectorizer = CountVectorizer()
    count_vectorizer.fit(bow_list)
    count_transform = count_vectorizer.transform(bow_list)
    soup_count_array = count_transform.toarray()
    count_matrix = pd.DataFrame(soup_count_array)
    return count_matrix


# Trims matrix to only include terms seen more than x amount of time (count_treshold)
def count_vect_trim(count_matrix, count_treshold):
    compact_matrix = count_matrix.loc[:, (count_matrix.sum(axis=0) > count_treshold)]
    return compact_matrix


# Uses trimmed word count matrix, and cosine similarity matrix to retrieve similarity scores in regards to the chosen movie
def get_sim_scores(chosen_movie, titles, cosine_sim):
    title = chosen_movie.replace(' ', '').lower()
    titles_clean = titles.apply(lambda x: str(x).replace(' ', '').lower())
    titles_clean = pd.Index(titles_clean)
    idx = titles_clean.get_loc(title)
    sim_list = list(enumerate(cosine_sim[idx]))
    return sim_list


# Applies the ratings to scale the similarity scores
# Work in Progress!!! Not Completed
# def apply_scalers(sim_list, ratings, scaler):
#    scaler.fit(ratings)
#    std_ratings = scaler.transform(ratings)
#    for idx in range(len(sim_list)):
#       sim_list[idx] = sim_list[idx] * (std_ratings[idx] / 10)
#    return sim_list


# Retrieves top 5 scores from similarity scores, along with additional movie info for the output
def top_5_list(sim_list, output_info):
    sim_list = sorted(sim_list, key=lambda x: x[1], reverse=True)
    top_5 = sim_list[0:6]
    top_5_indices = [i[0] for i in top_5]
    output = output_info.fillna(' ', inplace=False)
    return output.iloc[top_5_indices].reset_index(drop=True)


def main():
    #### Defining Variables ####
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

    # 3 - Creates a Word-Count Matrix
    count_matrix = count_vectorize(bow_list)

    # 4 - Trims Matrix for Less Computations
    count_treshold = 5
    compact_matrix = count_vect_trim(count_matrix, count_treshold)

    # 5 - Cosine Similarity
    cosine_sim = cosine_similarity(compact_matrix, compact_matrix)

    # 6 - Retrieves a list of similarity scores for the chosen movie
    sim_list = get_sim_scores(chosen_movie, titles, cosine_sim)

    # 7 - Applies scaled version of 'Tomatometer_rating' to the similarity scores list
    #scaler = StandardScaler()
    #sim_list_scaled = apply_scalers(sim_list, ratings, scaler)

    # 8 - Sorts and retrieves a top 5 list of hightest similarity scores
    top_5 = top_5_list(sim_list, output_info)
    print(top_5)
    return titles, cosine_sim


if __name__ == "__main__":
    titles, cosine_sim = main()
