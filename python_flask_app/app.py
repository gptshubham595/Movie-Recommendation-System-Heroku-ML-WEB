import flask
from flask_cors import CORS, cross_origin
from flask import request
import pandas as pd
from selenium.webdriver.chrome.options import Options
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os


chrome_options = webdriver.ChromeOptions()  
chrome_bin = os.environ.get('GOOGLE_CHROME_BIN')
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--no-sandbox")  
chrome_options.add_argument("--disable-dev-sh-usage")

chrome_options.binary_location = chrome_bin
driver=webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),chrome_options=chrome_options)  


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity  as cos_sim

app=flask.Flask(__name__)
cors=CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

df=pd.read_csv('movie_dataset.csv')

########################################
def get_title_from_index(index):
	return df[df.index == index]["title"].values[0]

def get_index_from_title(title):
	return df[df.title == title]["index"].values[0]
##################################################

def combine_features(row):
    return row['keywords'] + " " + row['cast'] + " " + row['genres'] + " " + row['director']

def fetch_list(movie_user_likes):
    ##Step 1: Read CSV File
    #print(df.head())

    #print(df.columns)
    ##Step 2: Select Features
    features=['keywords','cast','genres','director']
    ##Step 3: Create a column in DF which combines all selected features
    for feature in features:
        df[feature]=df[feature].fillna('')

    df["combined"]=df.apply(combine_features,axis=1)

    #print(df["combined"].head())

    ##Step 4: Create count matrix from this new combined column
    cv=CountVectorizer()

    count=cv.fit_transform(df["combined"])

    ##Step 5: Compute the Cosine Similarity based on the count_matrix
    similarity_score=cos_sim(count)
    #print(similarity_score)

    #movie_user_likes = "Avatar"

    ## Step 6: Get index of this movie from its title
    index=get_index_from_title(movie_user_likes)

    ## Step 7: Get a list of similar movies in descending order of similarity score
    movies_to_recommend_scores=list(similarity_score[index])

    numbers = list(range(len(movies_to_recommend_scores)))
    result = dict(zip(numbers, movies_to_recommend_scores))
    sorted_keys = sorted(result, key=result.get)
    sorted_keys=sorted_keys[::-1]
    
    ## Step 8: Print titles of first 50 movies
    movies_to_recommend_list=sorted_keys[1:10]

    movies_to_recommend=[]
    for i in movies_to_recommend_list:
        movies_to_recommend.append(get_title_from_index(i))

    return movies_to_recommend

########################################
import json

def sel(movie_list):
    img={}
    import lxml
    from lxml import html
    import requests

    for i in movie_list:
        try:
            u="https://www.google.com/search?q="+str(i)+"&tbm=isch"            
            r = requests.get(u)
            tree = lxml.html.fromstring(r.content)
            a = tree.xpath('//img[@class="t0fcAb"]')[0].attrib['src']
            img[i]=a
        except:
            img[i]=""
    return img

@app.route('/',methods=['GET'])
@cross_origin()
def home():

    movie_name=request.args['movie_name']
    # jsonString = json.dumps(fetch_list(movie_name))
    jsonString = json.dumps(sel(fetch_list(movie_name)))
    try:
        return jsonString
    except: 
        return 'ERR'

if __name__ == '__main__':
    app.debug = True
    app.run()