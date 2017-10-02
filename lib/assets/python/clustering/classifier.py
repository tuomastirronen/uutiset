# coding: utf-8

import nltk
import numpy as np
import itertools
import random
import pandas as pd
import pickle
import psycopg2
import sys
import string
from nltk.corpus import stopwords
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import GaussianNB, BernoulliNB

reload(sys)  
sys.setdefaultencoding('utf8')

stop = stopwords.words('finnish')

conn = psycopg2.connect("dbname='uutiset_development' host='localhost'")

try:
    df = pd.read_sql_query('SELECT guid, title, summary, click_bait from entries',con=conn)
except:
    print "Cannot select from entries"

# Shuffle data
df = df.sample(frac=1)

# Combine title and summary
df['text'] = df.title + df.summary

# Lowercase
df.text = df.text.str.lower()

# Remove stopwords
df['text'] = df['text'].apply(lambda x : ' '.join([item for item in string.split(x.lower()) if item not in stop]))

# Collect the bag of words
all_words = []
for index, row in df.iterrows():
	all_words.append(row.text.split(' '))

# Flatten
all_words = [j for i in all_words for j in i]

# Frequency Distribution
all_words = nltk.FreqDist(all_words)

word_features = list(all_words.keys())

def find_features(document):
	words = set(document)
	features = {}

	for w in word_features:
		features[w] = (w in words)

	return features

featuresets = []
for index, row in df.iterrows():
	featuresets.append([find_features(row.text.split(' ')), row.click_bait])

split = np.rint(len(df.index) * 0.5).astype(int)

training_set = featuresets[:split]
testing_set = featuresets[split:]

# classifier_f = open('lib/assets/python/clustering/naivebayes.pickle', 'rb')
# classifier = pickle.load(classifier_f) 
# classifier_f.close()

classifier = nltk.NaiveBayesClassifier.train(training_set)
print "NaiveBayesClassifier accuracy percent: ", (nltk.classify.accuracy(classifier, testing_set)) * 100

classifier.show_most_informative_features(30)

print classifier.classify(testing_set[1][0])