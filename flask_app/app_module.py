import pandas as pd
import numpy as np
from flask import Flask, redirect, render_template, request, url_for
import os


# 1. Cleans text data for given movie title
def CleanTitle(titles):
    print("Cleaning Text Features... ")
    cleaned = titles.replace(' ', '')
    cleaned = cleaned.replace('[^\w\s]','')
    cleaned = cleaned.lower()
    
    return cleaned

# 2. Cleans text data for all possibly movie titles
def CleanTitles(titles):
    print("Cleaning Text Features... ")
    titles.fillna(' ', inplace=True)
    cleaned = titles.apply(lambda x: str(x).replace(' ', ''))
    cleaned = cleaned.apply(lambda x: str(x).replace('[^\w\s]',''))
    cleaned = cleaned.apply(lambda x: str(x).lower())
    return cleaned

# 3. Loads .csv files into data frames given 2 urls
def ReadAppData(url1,url2):
    movies = pd.read_csv(url1)
    index_df = pd.read_csv(url2)

    return movies, index_df

# 4. Retrieves movie recommendation data from POST request 'clean_title'
def RetrieveRecs(clean_title, movies, index_df):
    output_df=pd.DataFrame([])
        # finds chosen movie index from dataset
    movie_idx = movies[movies['clean_titles'] == str(clean_title)].index.values
        # makes list of the index values from the top 5 movies based on the chosen movie
    index_list = index_df.iloc[movie_idx, :].values.tolist()
        # defines the information that will be displayed on site
    movies_info = movies[['movie_title', 'tomatometer_rating', 'directors', 'actors','genres']]
        # creates df of all output info from given movie and top 5
    for idx in index_list:
        rec_info = movies_info.iloc[idx,:]
        output_df = output_df.append(rec_info, ignore_index=True)
    output_df = pd.DataFrame(output_df)
    return output_df