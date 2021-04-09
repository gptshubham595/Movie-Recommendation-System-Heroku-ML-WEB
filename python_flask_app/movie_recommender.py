import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity  as cos_sim
###### helper functions. Use them when needed #######
def get_title_from_index(index):
	return df[df.index == index]["title"].values[0]

def get_index_from_title(title):
	return df[df.title == title]["index"].values[0]
##################################################

##Step 1: Read CSV File
df=pd.read_csv('movie_dataset.csv')
print(df.head())

print(df.columns)
##Step 2: Select Features
features=['keywords','cast','genres','director']
##Step 3: Create a column in DF which combines all selected features
for feature in features:
	df[feature]=df[feature].fillna('')

def combine_features(row):
	return row['keywords'] + " " + row['cast'] + " " + row['genres'] + " " + row['director']

df["combined"]=df.apply(combine_features,axis=1)

print(df["combined"].head())

##Step 4: Create count matrix from this new combined column
cv=CountVectorizer()

count=cv.fit_transform(df["combined"])

##Step 5: Compute the Cosine Similarity based on the count_matrix
similarity_score=cos_sim(count)
print(similarity_score)

movie_user_likes = "Avatar"

## Step 6: Get index of this movie from its title
index=get_index_from_title(movie_user_likes)

## Step 7: Get a list of similar movies in descending order of similarity score
movies_to_recommend_scores=list(similarity_score[index])
#movies_to_recommend_scores.sort()
#movies_to_recommend_scores=movies_to_recommend_index[::-1]

numbers = list(range(len(movies_to_recommend_scores)))
result = dict(zip(numbers, movies_to_recommend_scores))
sorted_keys = sorted(result, key=result.get)
sorted_keys=sorted_keys[::-1]
## Step 8: Print titles of first 50 movies
movies_to_recommend_list=sorted_keys[1:51]

movies_to_recommend=[]
for i in movies_to_recommend_list:
    movies_to_recommend.append(get_title_from_index(i))