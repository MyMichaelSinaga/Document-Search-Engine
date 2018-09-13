from nltk.corpus import wordnet as wn

#Buat query pencarian yang baru yang relevan dengan kueri yang lama
def synonym_list(processed_query):
	final_query_words = []
	for w in processed_query:
		syns = wn.synsets(w)
		names=[s.name().split('.')[0] for s in syns]
		if len(names)>=2:names=names[:2]
		names.append(w)
		for n in names:
			final_query_words.append(n)
	return final_query_words
synonyms = []

#tes cari sinonim
for syn in wn.synsets("good"):
   for l in syn.lemmas():
        synonyms.append(l.name())
        
#print(set(synonyms))