Movie Recommendation System

Overview:
This is a content-based recommendation system using Rotten Tomatoes data of over 17,000 different movies. 


File Structure:

flask_app/                * folder - contains entirety of Flask app
  __pycache__/            * folder - contains cache for app_modules
  templates/              * folder - contains all html files and branch files for the website
    base.html             * main branch of html templates - all other html files connect to this one
    developer_info.html   * html for developer_info
    explore_data.hmtl     * html for explore_data
    overview.html         * html for overview
    selection.html        * html for selection
  app_module.py           * module - contains functions for app.py
  app.py                  * script - Flask app
  app.yaml                * used for configuring work enviroment in Google Cloud App Engine
  requirements.txt        * lists dependencies for python scripts
  
main_process/                   * folder - contains the batch processing files
  data_files/                   * folder - contains the csv files needed
    RecIndices.csv              * created from main.py - lists index values of top 5 rec for every movie
    rotten_tomatoes_movies.csv  * original and uncleaned data from the source
  main_module.py                * module - contains functions for main.py
  main.py                       * script - processes, and uploads data to Cloud storage
  requirements.txt              * lists dependencies for python scripts
  service_key.json              * Google Cloud service key example - needed to upload to Cloud Storage

things to include: possible yaml file for main_process once deployed

