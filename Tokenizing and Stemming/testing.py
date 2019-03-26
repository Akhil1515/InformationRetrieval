# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 23:51:46 2018

@author: Akhil
"""


#    ----------------------------- TOKENIZATION ----------------------
from datetime import datetime # used to calculate the execution time
from nltk.tokenize import word_tokenize # used to divide strings into substrings
import re  # used to match or find other strings
import os,os.path
from collections import Counter # used to count hashable objects
import collections
import sys
from nltk.stem import PorterStemmer # used for stemming 

#DIR = '/people/cs/s/sanda/cs6322/Cranfield'
DIR = sys.argv[1]
start = datetime.now()
list1 = [name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))] # list1 gets all the 1400 files which are in cranfield 

count = 0 # keeps track of tokens count
l = []
for i in list1:
    filePath = DIR+i # relative path to the 1400 files
    file1 = open(filePath,"r")
    f1 = file1.read()
   
    rem = re.compile('<(.*?)>')
    k = re.sub(rem,'',f1)      # removes tags 
    k = re.sub('[\d]+'," ",k) # removes all digits 
    k = re.sub('[\W]+'," ",k) # removes all special characters
    k = word_tokenize(k) # tokenizes the documents
    k = [item.lower() for item in k] # converts Upper case to Lower case
    length = len(k)
    l.extend(k)
    
    count+= length

#to find unique words - set contains only unique words
s = set(l)

# list l contains all tokens and counter helps to find words that appeared only once
c = Counter(l)
indexes = [1 if c[item] ==1 else 0 for item in l]

# retrieve 30 most frequent words
fourth = collections.Counter(l).most_common(30)


print("The number of tokens in cranfield text collection: ", count)
print("The number of unique words in the cranfield text collection :", len(s))
print("The number of words that appeared only once in the cranfield text collection :", indexes.count(1))
print("The 30 most frequent words in the cranfield text collection:")
for i in fourth:
    print(i)
print("Average number of word tokens per document:", count/len(list1))

print("Time taken:", str(datetime.now()-start))





#    ------------------------  STEMMING      ------------------------------
count1 = 0
list2 = []
ps = PorterStemmer()
# perform stemming
for w in l:
    ab = ps.stem(w)
    ab = ab.encode("utf-8")
    list2.append(ps.stem(ab))
    count1+=1
# list 'list2' contains all stems and counter helps to find stems that appeared only once   
c1 = Counter(list2)
indexes1 = [1 if c1[item] ==1 else 0 for item in list2]

# retrieve 30 most frequent stems
fourth1 = collections.Counter(list2).most_common(30)

print("\n\n")
print("Number of distinct stems in cranfield collection:", len(set(list2)))
print("number of stems that occured once in cranfield collection: ", indexes1.count(1))
print("The 30 most frequent stems in the cranfield collection:")
for i in fourth1:
    print(i)
print("Average number of stems per document:", len(list2)/len(list1)) # avg number of stems per document
print("Average number of distinct stems per document:", len(set(list2))/len(list1)) # avg number of distinct stems per document


