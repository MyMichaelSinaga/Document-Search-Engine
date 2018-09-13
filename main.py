#import lib format
#import PyPDF2
#import docx2txt
#import gui lib
import tkinter
from tkinter import *
from tkinter import messagebox
import os
import numpy as np
import tokeniser as tkn
import spellcheck as sc
import webbrowser
def searchQuery(query,text_files,stats_dict,Number_of_docs,doc_list,idf_dict,list_of_words):
    
	processed_query = tkn.tokenise_normalise(query)#normalisasi kueri

	final_query = sc.synonym_list(processed_query)#tambahkan kueri yang relevan

	final_query = tkn.stem(final_query)#ubah kueri ke bentuk dasar

	print(processed_query)

	final_query = [x for x in final_query if x in stats_dict]
	if final_query!=[]:
		query_dict = tkn.create_tf_dict_query(final_query) #temukan term-frequency untuk setiap kata dalam query
		query_dict = tkn.find_tfidf_query(query_dict, idf_dict, Number_of_docs) #temukan tf-idf untuk setiap kata dalam query
		vector_array = np.zeros((len(query_dict.keys()), Number_of_docs))
		i=0
		j=0
		query_vector = np.zeros((1, len(query_dict.keys())))
    
		for w in query_dict:
		#buat vektor tf-idf untuk setiap pencarian kata dalam dokumen
			query_vector[0][i] = query_dict[w]
			for d in doc_list:
				if d not in stats_dict[w]:
					j += 1
				else :
					vector_array[i][j] = stats_dict[w][d]
					j += 1
			i += 1
			j = 0
	
		magnitude = np.linalg.norm(vector_array, axis = 0)#ubah vektor dokumen ke vektor satuan
		vector_array = np.divide(vector_array, magnitude)
		vector_array[np.isnan(vector_array)] = 0

		q_magnitude = np.linalg.norm(query_vector, axis = 1)#ubah vektor query ke vektor satuan
		query_vector = np.divide(query_vector, q_magnitude)

		dot_product = np.dot(query_vector, vector_array) #hitung nilai dot product dari setiap vektor dokumen dengan vektor query
		dot_product = dot_product.tolist()

		final_rank = list(zip(dot_product[0], doc_list))#sorting cosine scores untuk ranking semua dokumen.
		final_rank.sort(reverse = True)
		searchf=Tk()
		searchf.wm_title('4 Sejoli Search')
		blank='           '
		blanklabel=Label( searchf,text=blank*40,font=("ComicSansMS", 10))
		label1 = Label( searchf,text=query+'\n\n',font=("ComicSansMS", 20))
		label1.pack()
		blanklabel.pack()
		def callbacks(event):
			webbrowser.open_new(event.widget.cget("text"))
		for i in final_rank[:2]:
			labl=Label( searchf,text=i[1],font=("ComicSansMS", 12),justify=LEFT, fg="blue", cursor="hand2")
			labl.bind("<Button-1>", callbacks)
			labl.pack()
			
	else :messagebox.showinfo("Error Messsage", "Kueri tidak ditemukan")#jika query tidak ditemukan, tampilkan error message.

	
	
	
	
corpus_dir = "Dokumen" #Gunakan folder dokumen (berisi file .txt)


text_files = [os.path.join(corpus_dir, f) for f in os.listdir(corpus_dir)]
stats_dict = {}
Number_of_docs = len(text_files)
doc_list = []

for f in text_files:	#baca setiap file .txt
	doc = open(f, 'r')
	lines = [l.strip() for l in doc.readlines()]
	index = 0 
	full_transcript = []

	while True:
		if index >= len(lines):
			break
		line = lines[index]
		full_transcript.append(line)
		index += 1
	#tokenisasi dan ubah teks ke bentuk dasar
	processed_text = tkn.tokenise_normalise(full_transcript)
	processed_text = tkn.stem(processed_text)
	stats_dict = tkn.create_tf_dict_doc(processed_text, f, stats_dict)#buat sebuah dictionary untuk menampung setiap scores tf-idf
	doc_list.append(f)


stats_dict, idf_dict = tkn.find_tfidf_doc(stats_dict, Number_of_docs)

list_of_words = sorted(stats_dict.keys())
doc_list.sort()


#User Interface
top=Tk()
top.wm_title("4 Sejoli Search")
f = Frame(top, width=600,height=350)
f.pack(fill=X, expand=True)

e1=Entry(top,bd=6,width=40)
e1.insert(END, '')
e1.place(relx=0.5, rely=0.35, anchor=CENTER)
b1=Button(top,text="Search",command= lambda: searchQuery(e1.get(),text_files,stats_dict,Number_of_docs,doc_list,idf_dict,list_of_words))
b1.place(relx=0.5, rely=0.5, anchor=CENTER)
top.mainloop()
