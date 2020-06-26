"""
Module that is importing the data from the CSV file using the Panda,
then using the tf-idf to cluster all articles to 10 clusters using k-means
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer


data = pd.read_csv("output.csv")

stemmer = SnowballStemmer("english")
data['Stemmed'] = [stemmer.stem(x) for x in data['Text']]
vectorizer = TfidfVectorizer(min_df=.01, max_df=.5, stop_words='english', ngram_range=(1,2))
tvec_weights  = vectorizer.fit_transform(data.Stemmed.dropna())
weights = np.asarray(tvec_weights.mean(axis=0)).ravel().tolist()
weights_df = pd.DataFrame({'term': vectorizer.get_feature_names(), 'weight': weights})

kmeans = KMeans(n_clusters=10).fit(tvec_weights)
data['Cluster'] = [x for x in kmeans.labels_]

for index, row in data.iterrows():
    print(row['Title'], "-", row['Cluster'])
