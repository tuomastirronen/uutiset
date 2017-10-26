from sklearn.feature_extraction.text import TfidfVectorizer

class Document():
	@staticmethod
	def get_relevance(document, query):
		try:
			vect = TfidfVectorizer(min_df=1)
			tfidf = vect.fit_transform([document, query])
			pairwise_similarity = (tfidf * tfidf.T).A[0,1]			
		except Exception, e:
			print str(e)

		return pairwise_similarity