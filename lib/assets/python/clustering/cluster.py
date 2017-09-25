import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import sys

reload(sys)  
sys.setdefaultencoding('utf8')

data = pd.read_csv("lib/assets/python/clustering/entries.csv", names=['title', 'categories', 'summary'], delimiter = "|")

# documents = data.summary.astype('U').tolist()
documents = data.title.astype('U').tolist()

# vectorize the text i.e. convert the strings to numeric features
stop_words = [unicode(x.strip(), 'utf-8') for x in open('lib/assets/python/clustering/stopwords.txt','r').read().split('\n')]
vectorizer = TfidfVectorizer(stop_words=stop_words)
X = vectorizer.fit_transform(documents)

# cluster documents
true_k = 10
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)

predict = model.predict(X)

# in row_dict we store actual meanings of rows, in my case it's russian words
df = pd.DataFrame()

for i in range(predict.size):
  print predict[i], data.title[i]  
  df = df.append({'title': data.title[i], 'cluster': predict[i]}, ignore_index=True)  

for i in range(true_k):
  print 'cluster', i
  print df.loc[df['cluster'] == i]

