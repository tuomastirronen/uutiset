from __future__ import print_function
import nltk
from nltk.stem.snowball import SnowballStemmer
import numpy as np
import pandas as pd
import re
import os
import sys
import codecs
import mpld3
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans

reload(sys)  
sys.setdefaultencoding('utf8')

data = pd.read_csv('lib/assets/python/clustering/entries.csv', sep="|", names = ["title", "summary"])
stopwords = open("lib/assets/python/clustering/stopwords.txt", "r").read().split('\n')
stemmer = SnowballStemmer("finnish")

# here I define a tokenizer and stemmer which returns the set of stems in the text that it is passed

def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems


def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens

#not super pythonic, no, not at all.
#use extend so it's a big flat list of vocab
totalvocab_stemmed = []
totalvocab_tokenized = []
for i in data.summary:
    allwords_stemmed = tokenize_and_stem(str(i).decode('utf-8')) #for each item in 'synopses', tokenize/stem
    totalvocab_stemmed.extend(allwords_stemmed) #extend the 'totalvocab_stemmed' list
    
    allwords_tokenized = tokenize_only(str(i).decode('utf-8'))
    totalvocab_tokenized.extend(allwords_tokenized)


vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)
print('there are ', str(vocab_frame.shape[0]), ' items in vocab_frame')

#define vectorizer parameters
tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                 min_df=0.2, stop_words='english',
                                 use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,3))

tfidf_matrix = tfidf_vectorizer.fit_transform(data.summary.astype('U')) #fit the vectorizer to synopses

print(tfidf_matrix.shape)

terms = tfidf_vectorizer.get_feature_names()
dist = 1 - cosine_similarity(tfidf_matrix)

num_clusters = 5

km = KMeans(n_clusters=num_clusters)

km.fit(tfidf_matrix)

clusters = km.labels_.tolist()

from sklearn.externals import joblib

#uncomment the below to save your model 
#since I've already run my model I am loading from the pickle

joblib.dump(km,  'lib/assets/python/clustering/doc_cluster.pkl')

km = joblib.load('lib/assets/python/clustering/doc_cluster.pkl')
clusters = km.labels_.tolist()

entries = { 'title': data.title.tolist(), 'symmary': data.summary.tolist(), 'cluster': clusters }

frame = pd.DataFrame(entries, index = [clusters] , columns = ['title', 'cluster'])

print(frame['cluster'].value_counts()) #number of entries per cluster (clusters from 0 to 4)

print("Top terms per cluster:")
print()
#sort cluster centers by proximity to centroid
order_centroids = km.cluster_centers_.argsort()[:, ::-1] 

for i in range(num_clusters):
    print("Cluster %d words:" % i, end='')
    print() #add whitespace
    for ind in order_centroids[i, :6]: #replace 6 with n words per cluster
        print(' %s' % vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'))
        print() #add whitespace
    print() #add whitespace
    print() #add whitespace
    
    print("Cluster %d titles:" % i, end='')
    print() #add whitespace
    for title in frame.ix[i]['title'].values.tolist():
        print(' %s,' % title, end='')
        print() #add whitespace
    print() #add whitespace
    print() #add whitespace
    
print()
print()