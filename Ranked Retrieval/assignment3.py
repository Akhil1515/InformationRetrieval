import re					
import nltk					
import collections				
from collections import defaultdict
import time
import sys
import os
from os import listdir
from os.path import isfile, join
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import math


posting_lists = {}
ordered_dict_lemmas,query_dict = {},{}
coll_size,totlen = 0,0
cosine,cosine_value = 0,0
sum_norm1,sum_norm2 = 0,0
cos_order_w1,cos_order_w2 = {},{}
query = ""
query_lemmas,query_list,lemmas = [],[],[]
token_dict = {}
lemmatizer = WordNetLemmatizer()
weight1_query,weight2_query = {},{}
weight1_doc,weight2_doc = {},{}
weight1_fullqueries = []
weight1_fulldoc,weight2_fulldoc = [],[]
weight2_fullqueries = []
weight1_top_five = []
weight2_top_five = []
headline1 = []
value_list1 = [] 
value_list2 = []


mypath = sys.argv[1]
mypath1 = sys.argv[2]
filenames = [f for f in listdir(mypath) if isfile(join(mypath, f))]
filenames.sort()
avg_doclen1 = 98


inputfile = open(mypath1,"r")
queries = inputfile.readlines()
for i in range(0,len(queries)):
	if queries[i].startswith('Q'):
		j = i+1
		while j != len(queries) and queries[j] != "\n":
			query += queries[j]
			j += 1
		query_list.append(query)
		query = ""

def desc_tag(tag):

    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN



for i in range(0,len(filenames)):
	
    
    docid = i+1
    coll_size = coll_size + 1
    inputfiles = open(mypath+filenames[i],"r")
    k = inputfiles.read()
    headline1.append(k[(k.index('<TITLE>') + len('<TITLE>')):k.index('</TITLE>')])
    k = re.sub('<[^<]+>', " ", k)	
    k = re.sub('[\d]+', " ", k)
    k = re.sub('[\W]+', " ", k)
    k = nltk.word_tokenize(k.lower()) 

    processed_tokens = [word for word in k if word not in stopwords.words('english')]
    doclen = len(processed_tokens)
    totlen = totlen + doclen
    token_dict = dict(nltk.pos_tag(processed_tokens))

    for key,value in token_dict.items():
        lemmas.append(lemmatizer.lemmatize(key,desc_tag(value)).encode('utf-8'))

    lemmacount = collections.Counter(lemmas)
    maxtf = max(lemmacount.values())

    for word,tf in lemmacount.items():
        w1 = round((0.4 + 0.6 * math.log10(tf + 0.5)/math.log10(maxtf + 1.0)),3)
        weight1_doc[word] = w1	

        w2 = round((0.4 + 0.6 * (tf / (tf + 0.5 + 1.5 * (doclen / avg_doclen1)))),3)
        weight2_doc[word] = w2
    for word,tf in lemmacount.items():
        each_posting1 = [[docid,tf,maxtf,doclen]]
        if word in posting_lists:
            posting_lists[word].extend(each_posting1)
        else:
            posting_lists[word] = each_posting1
    lemmas = []
    weight1_fulldoc.append(weight1_doc)
    weight2_fulldoc.append(weight2_doc)
    weight1_doc,weight2_doc = {},{}

ordered_dict_lemmas= collections.OrderedDict(sorted(posting_lists.items()))


avg_doclen = totlen/coll_size

for i in range(len(query_list)):
	k1 = re.sub('[\d]+', " ", query_list[i])
	k1 = re.sub('[\W]+', " ", k1)
	query_tokens = nltk.word_tokenize(k1.lower())
	k1 = [word for word in query_tokens if word not in stopwords.words('english')]
	query_dict = dict(nltk.pos_tag(k1))
	for key,value in query_dict.items():
		query_lemmas.append(lemmatizer.lemmatize(key,desc_tag(value)).encode('utf-8'))
	query_doclen = len(query_lemmas)
	query_count = collections.Counter(query_lemmas)
	maxtf_query = max(query_count.values())
	for qterm,tf in query_count.items():
		for term, postings in ordered_dict_lemmas.items():
			if term == qterm:
				query_df = len(postings)  

		w1 = round((0.4 + 0.6 * math.log10(tf + 0.5)/math.log10(maxtf_query + 1.0)) * (math.log10(coll_size / query_df) / math.log10(coll_size)),3)
		weight1_query[qterm] = w1	

		w2 = round((0.4 + 0.6 * (tf / (tf + 0.5 + 1.5 * (query_doclen / avg_doclen))) * math.log10(coll_size / query_df) / math.log10(coll_size)),3)
		weight2_query[qterm] = w2	
	weight1_fullqueries.append(weight1_query)
	weight2_fullqueries.append(weight2_query)
	weight1_query = {} 
	weight2_query = {} 
	query_lemmas = []

for i in range(coll_size):
	for key,value in weight1_fulldoc[i].items():
		sum_norm1 += value**2
	sum_norm1 = math.sqrt(sum_norm1)
	for key,value in weight1_fulldoc[i].items():
		weight1_fulldoc[i][key] = round(value / sum_norm1,3)
	for key,value in weight2_fulldoc[i].items():
		sum_norm2 += value**2
	sum_norm2 = math.sqrt(sum_norm2)
	for key,value in weight2_fulldoc[i].items():
		weight2_fulldoc[i][key] = round(value / sum_norm2,3)
	sum_norm1,sum_norm2 = 0,0
	

for i in range(len(query_list)):
	for key,value in weight1_fullqueries[i].items():
		sum_norm1 += value**2
	sum_norm1 = math.sqrt(sum_norm1)
	for key,value in weight1_fullqueries[i].items():
		weight1_fullqueries[i][key] = round(value / sum_norm1,3)
	for key,value in weight2_fullqueries[i].items():
		sum_norm2 += value**2
	sum_norm2 = math.sqrt(sum_norm2)
	for key,value in weight2_fullqueries[i].items():
		weight2_fullqueries[i][key] = round(value / sum_norm2,3)
	sum_norm1,sum_norm2 = 0,0
	

print("\n VECTOR REPRESENTATION OF QUERIES ACCORDING TO WEIGHING SCHEME W1: \n")
for i in range(len(query_list)):
    print("(Q"+str(i+1)+": "+str(weight1_fullqueries[i])+") \n")
    
print("\n VECTOR REPRESENTATION OF QUERIES ACCORDING TO WEIGHING SCHEME W2: \n")
for i in range(len(query_list)):
    print("(Q"+str(i+1)+":"+str(weight2_fullqueries[i])+") \n")
    

print("TOP 5 DOCUMENTS FOR THE QUERY UNDER WEIGHING SCHEMES W1 & W2")
for i in range(len(query_list)):
    
    
	
    for j in range(coll_size):
        for key,value in weight1_fullqueries[i].items():
            for key1,value1 in weight1_fulldoc[j].items():
                if key == key1:
                    cosine = value * value1
            cosine_value = cosine_value + cosine
        name = 'Q' + str(i+1) + ',D' + str(j+1)
        cos_order_w1[name] = round(cosine_value,5)
        cosine_value = 0
        for key,value in weight2_fullqueries[i].items():
            for key1,value1 in weight2_fulldoc[j].items():
                if key == key1:
                    cosine = value * value1
            cosine_value += cosine
        name = 'Q' + str(i+1) + ',D' + str(j+1)
        cos_order_w2[name] = round(cosine_value,5)
        cosine_value = 0
    print("Weight W1: ",dict(collections.Counter(cos_order_w1).most_common(5)))
    weight1_top_five.append(list(dict(collections.Counter(cos_order_w1).most_common(5)).keys()))
    value_list1.append(list(dict(collections.Counter(cos_order_w1).most_common(5)).values()))
    print("Weight W2: ",dict(collections.Counter(cos_order_w2).most_common(5)))
    weight2_top_five.append(list(dict(collections.Counter(cos_order_w2).most_common(5)).keys()))
    value_list2.append(list(dict(collections.Counter(cos_order_w2).most_common(5)).values()))
    cos_order_w1,cos_order_w2 = {},{}
    
    
    
for i in range(0,len(weight1_top_five)):
	print("Query"+ str(i+1) +" Characteristics for weight1 :")
	print("rank \t score \t external document identifier \t headline")
	for j in range(0,5):
		weight1_top_five[i][j] = int(weight1_top_five[i][j].split('D')[1]) - 1
		print(str(j+1)+"\t"+str(value_list1[i][j])+"\t"+str(weight1_top_five[i][j] + 1)+"\t"+headline1[weight1_top_five[i][j]])
        
        
for i in range(0,len(weight2_top_five)):
	print("Query"+ str(i+1) +" Characteristics for weight2 :")
	print("rank \t score \t external document identifier \t headline")
	for j in range(0,5):
		weight2_top_five[i][j] = int(weight2_top_five[i][j].split('D')[1]) - 1
		print(str(j+1)+"\t"+str(value_list2[i][j])+"\t"+str(weight2_top_five[i][j] + 1)+"\t"+headline1[weight2_top_five[i][j]])
        
        
for i in range(0,len(weight1_top_five)):
	print("Document Vector for Query"+str(i+1)+" weight1: ")
	for j in range(0,5):
		print("For Document"+str(weight1_top_five[i][j]+1) + " vector representation")		
		print(weight1_fulldoc[weight1_top_five[i][j]])
	print("\n\n")

for i in range(0,len(weight2_top_five)):
	print("Document Vector for Query"+str(i+1)+" weight2: ")
	for j in range(0,5):
		print("For Document"+str(weight2_top_five[i][j]+1) + " vector representation  ")		
		print(weight2_fulldoc[weight2_top_five[i][j]])
	print("\n\n")
    
    
    
    
	
    