from app_module import CleanTitle, CleanTitles, ReadAppData, RetrieveRecs
from flask import Flask, redirect, render_template, request, url_for
import pandas as pd
import numpy as np
import os


app = Flask(__name__)

@app.route("/")
def overview():
    return render_template("overview.html")

@app.route("/selection", methods=["POST","GET"])
def selection():
    # Creates empty dataframe to be filled with movie data to be displayed
    if request.method == "POST":
            # Original dataset
        url1 = 'gs://movie_rec_bucket/rotten_tomatoes_movies.csv'
            # Processed data
        url2 = 'gs://movie_rec_bucket/RecIndices.csv'
        movies, index_df = ReadAppData(url1,url2)

        title = request.form['userMovie']
            # title is cleaned to cross reference all titles in dataset
        clean_title = CleanTitle(title)
            # cleans all titles in dataset
        movies['clean_titles'] = CleanTitles(movies['movie_title'])
            # if chosen movie is found in dataset
        if movies['clean_titles'].str.contains(clean_title).any():
            output_df = RetrieveRecs(clean_title=clean_title, movies=movies, index_df=index_df)
            success = "You selected: "
            return render_template("selection.html", display_df=output_df, message=success)
        else: # Failure to find movie

            output_df = pd.DataFrame([]) # nothing to display
            fail = "Could not find movie, try again and double check spelling"
            return render_template("selection.html", display_df=output_df, message=fail)
    else: # Loaded first, before POST

        output_df = pd.DataFrame([]) # nothing to display
        test_msg = "Can't find the movie you're looking for? Try these classics: Toy Story, Pulp Fiction, or Forrest Gump"
        return render_template("selection.html", display_df=output_df, message=test_msg)

@app.route("/explore_data")
def explore_data():
    return render_template("explore_data.html")

@app.route("/developer_info")
def developer_info():
    return render_template("developer_info.html")


if __name__ == "__main__":
    app.run(debug=True, host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 4444)))


# python ./App.py
# http://127.0.0.1:4444/