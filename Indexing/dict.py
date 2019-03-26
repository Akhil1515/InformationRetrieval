# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 13:23:59 2018

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
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import nltk
import operator
import pickle

lemmatizer = nltk.WordNetLemmatizer()
ps = PorterStemmer()

#DIR = 'E:/MS in UTD/Sem 1/Information Retrieval/Homework-2/cranfield/'
#DIR = '/people/cs/s/sanda/cs6322/Cranfield'
DIR = sys.argv[1]

list1 = [name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))] # list1 gets all the 1400 files which are in cranfield 

l = []
d1={}
d2={}
docmaxtf = []
docLenlist = []
count1 = 0
docList = []
start1 = datetime.now()
for i in list1:
    count1 = count1 + 1
    filePath = DIR+i # relative path to the 1400 files
    file1 = open(filePath,"r")
    f1 = file1.read()
   
    rem = re.compile('<(.*?)>')
    k = re.sub(rem,'',f1)      # removes tags 
    k = re.sub('[\d]+'," ",k) # removes all digits 
    k = re.sub('[\W]+'," ",k) # removes all special characters
    k = word_tokenize(k) # tokenizes the documents
    k = [item.lower() for item in k] # converts Upper case to Lower case
    docLen = len(k)
    docList.append((count1,docLen))
        
    words_without_stopwords = [w for w in k if w not in stopwords.words('english')]
    
    # LEMMATIZER
    lemmas_list = []
    for var in words_without_stopwords:
        lemmas = lemmatizer.lemmatize(var)
        lemmas_list.append(lemmas)
    
    lc = collections.Counter(lemmas_list)
    mostFrequentTermLemma = lc.most_common(1)
    for key, value in mostFrequentTermLemma:
        max_tf_lemma = value
        docmaxtf.append((count1,max_tf_lemma))
        
    for term, termfreq in lc.items():
        abcd = [count1, termfreq,max_tf_lemma,docLen]
        dictlist=[]
        if term in d1:
            d1[term].append(abcd)
        else:
            dictlist.append(abcd)
            d1[term] = dictlist
            
dictLemma = collections.OrderedDict(sorted(d1.items()))


nof1 = 0
for term in dictLemma.items():
    nof1+=1
    
with open('Index_Version1_uncompressed.txt', 'w') as file:
    file.write("Term \t DF \t [DocId, TF, MaxTF, DocLen] \n")
    for term, tf in dictLemma.items():
        docFreq = str(len(tf))
        file.write(term+":\t")
        file.write(docFreq+"\t")
        file.write(str(tf))
        file.write("\n")

with open("Index_Version1_uncompressed.txt",'r') as txtfile:
    myString = txtfile.read()
ofile = open("Index_Version_1.uncompressed.bin",'wb')
pickle.dump(myString, ofile)
ofile.close()


end1 = datetime.now()

count2 = 0        
start2 = datetime.now()   
for i in list1:
    count2 = count2 + 1
    filePath = DIR+i # relative path to the 1400 files
    file1 = open(filePath,"r")
    f1 = file1.read()
   
    rem = re.compile('<(.*?)>')
    k = re.sub(rem,'',f1)      # removes tags 
    k = re.sub('[\d]+'," ",k) # removes all digits 
    k = re.sub('[\W]+'," ",k) # removes all special characters
    k = word_tokenize(k) # tokenizes the documents
    k = [item.lower() for item in k] # converts Upper case to Lower case
    docLen = len(k)
        
    words_without_stopwords = [w for w in k if w not in stopwords.words('english')]
    
    #STEMMING
    stems_list = []
    for w in words_without_stopwords:
        stems1 = ps.stem(w)
        stems1 = stems1.encode("utf-8")
        stems_list.append(stems1)
        
    lc1 = collections.Counter(stems_list)
    mostFrequentTermStems = lc1.most_common(1)
    for key, value in mostFrequentTermStems:
        max_tf_Stems = value
        
    for term, termfreq in lc1.items():
        abcde = [count2, termfreq,max_tf_Stems,docLen]
        dictlist_stems=[]
        if term in d2:
            d2[term].append(abcde)
        else:
            dictlist_stems.append(abcde)
            d2[term] = dictlist_stems

dictStems = collections.OrderedDict(sorted(d2.items()))   

nof2 = 0
for term in dictStems.items():
    nof2+=1
     
with open('Index_Version2_uncompressed.txt', 'w') as file:
    file.write("Term \t DF \t [DocId, TF, MaxTF, DocLen] \n")
    for term, tf in dictStems.items():
        docFreq = str(len(tf))
        file.write(term+":\t")
        file.write(docFreq+"\t")
        file.write(str(tf))
        file.write("\n")

with open("Index_Version2_uncompressed.txt",'r') as txtfile:
    myString1 = txtfile.read()
ofile1 = open("Index_Version_2.uncompressed.bin",'wb')
pickle.dump(myString1, ofile1)
ofile1.close()   
     
end2 = datetime.now()


start3 = datetime.now()  
# Compressed index 1
termStringCompress1 = ""
for term, tf in dictLemma.items():
    termStringCompress1 = termStringCompress1 + str(len(term)) + term


termString = ""
with open('IndexVersion1Compressed.txt', 'w') as file:
    def gamma(number):
      binaryNum = str(bin(number))
      offset = binaryNum[3:]
      offsetLen = len(offset)
      length = unary(offsetLen)
      gammaString = str(length) + str(offset)
      return gammaString
    
    def unary(number):
        unaryString = ""
        i = 0
        while i < number:
            unaryString = unaryString + str(1)
            i += 1
        unaryString = unaryString + str(0)
        return unaryString

    termCounter = 0
    file.write("\nTerm String:\n"+termStringCompress1+"\n")
    for term, tf in dictLemma.items():
        termCounter = termCounter + 1
        listDocs = []
        listGaps = []
        for ele in tf:
            listDocs.append(ele[0])
        for ele in listDocs[:1]:
            listGaps.append(ele)
            
        for x in range((len(listDocs)-1)):
            listGaps.append( listDocs[x+1] - listDocs[x])
        binaryString = ""
        for ele in listGaps:
            gammaCode = str(gamma(ele))
            binaryString = binaryString + gammaCode
        file.write("\n"+binaryString+"\n")    
        
        termString = termString + str(len(term)) + term
        if (termCounter % 8 == 0):
            index = len(termString)
            file.write("\n"+str(index)+"\n")

with open("IndexVersion1Compressed.txt",'r') as txtfile:
    myString2 = txtfile.read()
ofile2 = open("Index_Version_1.compressed.bin",'wb')
pickle.dump(myString2, ofile2)
ofile2.close()   

end3 = datetime.now()

start4 = datetime.now()            
# Compressed index 2
termStringCompress2 = ""
for term, tf in dictLemma.items():
    termStringCompress2 = termStringCompress1 + str(len(term)) + term

termString = ""
with open('IndexVersion2Compressed.txt', 'w') as file:
    def gamma(number):
      binaryNum = str(bin(number))
      offset = binaryNum[3:]
      offsetLen = len(offset)
      length = unary1(offsetLen)
      gammaString = str(length) + str(offset)
      return gammaString
    
    def unary1(number):
        unaryString = ""
        i = 0
        while i < number:
            unaryString = unaryString + str(1)
            i += 1
        unaryString = unaryString + str(0)
        return unaryString
    
    def delta(number):
        binaryNum = str(bin(number))
        offset = binaryNum[2:]
        offsetLen = len(offset)
        length = gamma(offsetLen)
        finalOffset = binaryNum[3:]
        deltaString = str(length) + str(finalOffset)
        return deltaString    

    termCounter = 0
    file.write("\nTerm String:\n"+termStringCompress2+"\n")
    for term, tf in dictStems.items():
        termCounter = termCounter + 1
        listDocs = []
        listGaps = []
        for ele in tf:
            listDocs.append(ele[0])
        for ele in listDocs[:1]:
            listGaps.append(ele)
            
        for x in range((len(listDocs)-1)):
            listGaps.append( listDocs[x+1] - listDocs[x])
        binaryString = ""
        for ele in listGaps:
            deltaCode = str(delta(ele))
            binaryString = binaryString + deltaCode
        file.write("\n"+binaryString+"\n")    
with open("IndexVersion2Compressed.txt",'r') as txtfile:
    myString3 = txtfile.read()
ofile3 = open("Index_Version_2.compressed.bin",'wb')
pickle.dump(myString3, ofile3)
ofile3.close()           
end4 = datetime.now()




print("Elapsed time to build uncompressed Inverted index using lemmatization:", end1-start1)
print("Elapsed time to build uncompressed Inverted index using stemming:", end2-start2)
print("Elapsed time to build compressed Inverted index using lemmatization:", end3-start3)
print("Elapsed time to build compressed Inverted index using stemming:", end4-start4)

print("Size of index version1 :",os.path.getsize('Index_Version_1.uncompressed.bin'))
print("Size of index version2:",os.path.getsize('Index_Version_2.uncompressed.bin'))
print("Size of index version1 :",os.path.getsize('Index_Version_1.compressed.bin'))
print("Size of index version2:",os.path.getsize('Index_Version_2.compressed.bin'))

print("No. of inverted lists in index version1 uncompressed: ", nof1)
print("No. of inverted lists in index version2 uncompressed: ", nof2)
print("No. of inverted lists in index version1 compressed: ", nof1)
print("No. of inverted lists in index version2 compressed: ", nof2)


termsgiven = ["reynolds", "nasa", "prandtl", "flow", "pressure", "boundary", "shock"] 
for term,value in dictLemma.items():
    if term in termsgiven:
        size1 = sys.getsizeof(value)
        docf = str(len(value))
        print("\n")
        print("Term: ", term)
        print("Doc freq:",docf)
        tf = 0
        for i in value:
            tf += i[1]
        print("Term frequency is: ", tf)
        print("Inverted list size: ", size1)
      
for term,value in dictLemma.items():
    if term == 'nasa':
        print("Term:",term)
        docf = str(len(value))
        print("Doc frequency for ", term ,"is: ",docf)
        countP = 0
        for i in value[:3]:
            countP+=1
            termFre = i[1]
            docLen = i[3]
            max_tf = i[2]
            print("\nNasa Posting list entry :", countP)
            print("Term Frequency: ",termFre)
            print("Document length: " , docLen)
            print("Max term frequency: " , max_tf)
        
dictIndex1 ={}
for term, tf in dictLemma.items():
    docFreq = len(tf)
    dictIndex1[term] = docFreq
    
maxValIndex1 = max(dictIndex1.values())
minValIndex1 = min(dictIndex1.values())
maxTermsIndex1 = []
minTermsIndex1 = []
for k, v in dictIndex1.items():
    if dictIndex1[k] == maxValIndex1:
        maxTermsIndex1.append(k)
    elif dictIndex1[k] == minValIndex1:
        minTermsIndex1.append(k)
print("\nTerms from index 1 with largest df:")
print(maxTermsIndex1)
print("\nTerms from index 1 with smallest df:")
print(minTermsIndex1)   

dictIndex2 ={}
for term, tf in dictStems.items():
    docFreq = len(tf)
    dictIndex2[term] = docFreq
    
maxValIndex2 = max(dictIndex2.values())
minValIndex2 = min(dictIndex2.values())
maxTermsIndex2 = []
minTermsIndex2 = []
for k, v in dictIndex2.items():
    if dictIndex2[k] == maxValIndex2:
        maxTermsIndex2.append(k)
    elif dictIndex2[k] == minValIndex2:
        minTermsIndex2.append(k)
print("\nTerms(stems) from index 2 with largest df:")
print(maxTermsIndex2)
print("\nTerms(stems) from index 2 with smallest df:")
print(minTermsIndex2)   

docMaxtfDict = dict(docmaxtf)
maxtfDocId = max(docMaxtfDict.items(), key=operator.itemgetter(1))[0]
print("\nDocument id with the largest max_tf in collection: %s" % maxtfDocId)

maxdocLengthDict = dict(docList)
maxDocLenDocId = max(maxdocLengthDict.items(), key=operator.itemgetter(1))[0]
print("\nDocument id with the largest doc length in collection: %s" % maxDocLenDocId)

os.remove('Index_Version1_uncompressed.txt')
os.remove('Index_Version2_uncompressed.txt')
os.remove('IndexVersion1Compressed.txt')
os.remove('IndexVersion2Compressed.txt')