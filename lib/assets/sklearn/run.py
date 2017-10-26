#!/usr/bin/python
# -*- coding: UTF-8 -*-
import csv

from document import Document

import feedparser
from newspaper import Article
from langdetect import detect
import iso639

import string
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer("german")

keywords = []
reader = csv.reader(open('data/keywords.csv', 'rU'), delimiter=";", dialect=csv.excel_tab)
for row in reader:
	if len(row[1]) > 0:
		keywords.append(row[1])

# keywords = ['bank']

# Get data
data = feedparser.parse('http://www.nzz.ch/finanzen.rss')
print len(data['entries']), "entries"


documents = []
results = []

for entry in data['entries']:
	# Read the article
	article = Article(entry.link)
	article.download()
	article.parse()
	document = article.text
	words = word_tokenize(document)

	print "reading article", article.title
	# Remove punctuation
	words = [word.lower() for word in words if word.isalpha()]

	# Get language
	try:
		language = iso639.find(detect(entry.title))['name'].lower()
		stemmer = SnowballStemmer(language)
	except Exception, e:
		print str(e)
		stemmer = SnowballStemmer("english")
		print "stem language is set to english"

	# Stem text
	for word in words:
		word = stemmer.stem(word)	

	document = ' '.join(words)
	
	for keyword in keywords:		
		relevance = Document.get_relevance(document, stemmer.stem(keyword))
		if relevance > 0:
			results.append([keyword, relevance, entry.link])
	
results = sorted(results, key=lambda x: (x[0]), reverse=True)

print len(results), "results"

for result in results:
	print result[0], result[2], result[1]
