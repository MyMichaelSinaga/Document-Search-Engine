import math
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer # Anda dapat menggunakan stemmer lain seperti SnowballStemmer

#Tokenisasi setiap string dan ubah lakukan normalisasi
def tokenise_normalise(raw_string):
	tokenizer = RegexpTokenizer(r'\w+')
	tokenised_text = tokenizer.tokenize(str(raw_string))
	token_normalise = []
    
	for w in tokenised_text:
		w = w.lower()
		token_normalise.append(w)
	return token_normalise

#Ubah string ke bentuk dasar, misalnya: having -> have
def stem(token_normalised_text):
	processed_text = []
	stemmer = PorterStemmer()

	for w in token_normalised_text:
		root = stemmer.stem(w)
		root = str(root)
		processed_text.append(root)
	return processed_text
	
#Hitung setiap term-frequency (bobot kata) dalam satu dokumen
def create_tf_dict_doc(processed_text, f, stats_dict):
	for root in processed_text:
		if root not in stats_dict:		
			stats_dict[root] = {}
			stats_dict[root][f] = 1	
		if f not in stats_dict[root]:
			stats_dict[root][f] = 1
		stats_dict[root][f] += 1
	return stats_dict
	
#Hitung tf-idf scores untuk setiap query yang dicari	
def create_tf_dict_query(processed_query):
	query_dict = {}
	for root in processed_query:
		if root not in query_dict:	
			query_dict[root] = 1	
		query_dict[root] += 1
	return query_dict
		
#temukan skor idf untuk kata dalam dokumen dan perbarui nilai tf-idf yang telah ada	
def find_tfidf_doc(stats_dict, Number_of_docs):	
	idf_dict = {}
	for word in stats_dict:
		idf_dict[word] = len(stats_dict[word].keys())
        
	for word in stats_dict:
		for doc in stats_dict[word]:
			stats_dict[word][doc] = (1 + math.log(stats_dict[word][doc]))*math.log(Number_of_docs/idf_dict[word])
	return stats_dict, idf_dict

#temukan nilai tf-idf untuk kata dalam query pencarian perbarui nilai tf-idf yang telah ada
def find_tfidf_query(query_dict, idf_dict, Number_of_docs):
	for word in query_dict:
		query_dict[word] = (1 + math.log(query_dict[word]))*math.log(Number_of_docs/idf_dict[word])

	return query_dict