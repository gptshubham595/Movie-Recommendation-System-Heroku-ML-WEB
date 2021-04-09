from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.metrics.pairwise import cosine_similarity as cos_sim

text=["London Paris London","Paris Paris London"]


cv=CountVectorizer()
count=cv.fit_transform(text)

# print(count.toarray())
similarity_score=cos_sim(count)

print(similarity_score)


