import pandas as pd
import numpy as np
import string
import re
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from google.cloud import storage
import os
# 1 - Retreives .csv file from Google Cloud Storage Bucket
def ReadData(url):
    movies = pd.read_csv(url)
    return movies
# 2 - Cleans text features
def CleanText(text):
    print("Cleaning Text Features... ")
    clean_features = text.fillna(' ', inplace=False)
    for col in clean_features:
        clean_features[col] = clean_features[col].apply(lambda x: str(x).replace(' ', ''))
        clean_features[col] = clean_features[col].apply(lambda x: str(x).replace(',', ' '))
        clean_features[col] = clean_features[col].apply(lambda x: str(x).lower())
        clean_features[col] = clean_features[col].apply(lambda x: str(x).replace('&', ''))
        clean_features[col] = clean_features[col].apply(lambda x: str(x).replace('.', ''))
    return clean_features
# 3 - Creates a Bag-of-Words for each movie
def CreateBow(clean_text):
    print("Creating Bag-of-Words... ")
    bow_list = clean_text.agg(' '.join, axis=1)
    # for loop removes duplicate words within each movie's BoW
    for bow in bow_list:
        re.sub(r'\b(.+)\s+\1\b', r'\1', str(bow_list))
    return bow_list
# 4 - Creates a word-count matrix from the bag-of-words list
    # A word-count matrix will record the frequency of words across the dataset
    # Keep in mind, most of the text data include unique terms like actors, directors, and movie titles.
def CountVectorize(bow_list):
    print("Converting BoW to Matrix...")
    count_vectorizer = CountVectorizer()
    count_vectorizer.fit(bow_list)
    count_transform = count_vectorizer.transform(bow_list)
    soup_count_array = count_transform.toarray()
    count_matrix = pd.DataFrame(soup_count_array)
    return count_matrix
# 5 - Trims matrix to only include terms seen more than x amount of time (count_treshold)
def TrimMatrix(count_matrix, count_treshold):
    print("Trimming Matrix (May Take a Few Minutes)...")
    compact_matrix = count_matrix.loc[:, (count_matrix.sum(axis=0) > count_treshold)]
    return compact_matrix
# 6 - Calculates similarities between each movie
def SimilarityScores(matrix):
    print("Calculating Similarity Scores (Also May Take a Few Minutes)...")
    sim_df = cosine_similarity(matrix,matrix)
    return sim_df
# 7 - Sorts and saves top 15 similarity scores for each movie,
# then sorts the top 15 by Tomatometer Rating (High to Low).
# The function will then provide top 5 ratings from the most similar movies
def CreateRecDf(sim_df, ratings):
    print("Creating Top Recommendations From Sim Scores...")
    index_df=pd.DataFrame([])
    ratings_list= ratings.values.tolist()
    for col in range(len(sim_df)):
        sim_list=sim_df[col]
        movie_df=pd.DataFrame({
        'sim_score': sim_list,
        'rating': ratings_list
        })
        sim_sort = movie_df.sort_values(by = 'sim_score', ascending=False)
        top10 = sim_sort[1:11]
        top10_sort = top10.sort_values(by = 'rating', ascending=False)
        top5 = top10_sort[0:5]
        idx_list = pd.DataFrame(top5.index.values)
        idx_list = idx_list.transpose()
        index_df = index_df.append(idx_list)
    index_df=pd.DataFrame(index_df)
    index_df.columns=['rec1','rec2','rec3','rec4','rec5']
    index_df.reset_index(inplace=True,drop=True)
    return index_df
# 8 - Saves as .csv to (path)/data_files folder
def SaveCsv(index_df):
    print("Saving to .csv File...")
    index_df.to_csv('./main_process/data_files/RecIndices.csv')
    return
# 9 - Upload .csv to Google Cloud Storage bucket
def UploadCsv(blob_name, file_path, bucket_name):
    print('Uploading to Google Cloud Storage Bucket...')
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service_key.json'
    storage_client = storage.Client()
    dir(storage_client)
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        return True
    except Exception as e:
        print(e)
        return False