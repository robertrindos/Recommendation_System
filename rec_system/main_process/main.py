from main_module import ReadData, CleanText, CreateBow, CountVectorize, TrimMatrix, SimilarityScores, CreateRecDf, SaveCsv, UploadCsv
import pandas as pd
import numpy as np
import string
import re
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from google.cloud import storage
import os

def main():
        # Defining  URL to read .csv file
    url = 'gs://movie_rec_bucket/rotten_tomatoes_movies.csv'
    movies = ReadData(url)
    
        # Defining text features for Word-Count Matrix
    text_features = movies[['genres', 'directors', 'authors', 'actors', 'production_company', 'content_rating']]

        # Defining Rotten Tomatoes Ratings
    ratings = movies[['tomatometer_rating']]

        # 1 - CleanText()
    clean_text = CleanText(text_features)

        # 2 -  CreateBow()
    bow_list = CreateBow(clean_text)

        # 3 - CountVectorize()
    count_matrix = CountVectorize(bow_list)

        # 4 - TrimMatrix() - Only includes words that appear X amount of times across all movies
    minimum_freq = 5
    trimmed_matrix = TrimMatrix(count_matrix, minimum_freq)

        # 5 - SimilarityScores()
    sim_df = SimilarityScores(trimmed_matrix)

        # 6 - CreateRecDf()
    recommendation_df = CreateRecDf(sim_df, ratings)

        # 7 - SaveCsv()
    SaveCsv(recommendation_df)

        # 8 - UploadCsv()
    file_path = r'./main_process/data_files'
    UploadCsv('RecIndices.csv', os.path.join(file_path, 'RecIndices.csv'), 'movie_rec_bucket')

    print("All Done!")

if __name__ == "__main__":
    main()
