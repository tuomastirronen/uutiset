# coding: utf-8

import pandas as pd
import psycopg2
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import sys
from datetime import datetime, timedelta
import os
import urlparse

reload(sys)
sys.setdefaultencoding('utf8')

url = os.environ['DATABASE_URL']
# url = 'postgresql://postgres:postgres@localhost/uutiset_development'

result = urlparse.urlparse(url)

username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname

conn = psycopg2.connect(
    database = database,
    user = username,
    password = password,
    host = hostname
)

try:
	query = """ 
		SELECT "guid", "title", "summary", "categories", "click_bait"
		FROM "entries" 
		WHERE "click_bait" = false AND "published" >= %(filter)s
	"""
	query_params = {'filter': datetime.today() - timedelta(days=2)}

	data = pd.read_sql_query(query, con=conn, params=query_params)	
except:
	print "Cannot select from entries"

data['text'] = data.title + " " + data.summary + " " + data.categories
documents = data.text.astype('U').tolist()

# vectorize the text i.e. convert the strings to numeric features
stop_words = [unicode(x.strip(), 'utf-8') for x in open('lib/assets/classifier/data/stopwords.txt','r').read().split('\n')]
vectorizer = TfidfVectorizer(stop_words=stop_words)
X = vectorizer.fit_transform(documents)

# cluster documents
true_k = 5
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=200, n_init=1)
model.fit(X)

predict = model.predict(X)

df = pd.DataFrame()

for i in range(predict.size):	
	df = df.append({'summary': data.summary[i], 'cluster': predict[i]}, ignore_index=True)  

# Save data
data = {}  
data['clusters'] = []

with open('lib/assets/classifier/data/clusters.json','r+') as f:	
	for i in range(true_k):
		content = df.summary.loc[df['cluster'] == i].str.cat(sep=' ')
		cluster = {'id': i, 'content': content}
		data['clusters'].append(cluster)

with open('lib/assets/classifier/data/clusters.json', 'w') as outfile:  
    json.dump(data, outfile)