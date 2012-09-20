'''
Created on 2012-5-30

@author: guoxc
'''
import nltk
import csv
import re
import cPickle
from nltk.corpus import stopwords
file = open("../../data/raw-data1.csv","rb")
sw = stopwords.words("english")
c = csv.reader(file)
porter = nltk.PorterStemmer()
wnl = nltk.WordNetLemmatizer()
count = 0
term_dict = []
dict = {}
term_list = []
for l in c:
    count += 1
#    if count > 20:
#        break
    r = l[1] + l[2]
    r = r.lower()
#    rl = nltk.regexp_tokenize(r, r'''(?x)([A-Z]\.)+|\w+(-\w+)*|\$?\d+(\.\d+)?%?|\.\.\.|[][.,;'"?():-_']""')
    rl = re.split(r'\W+',r)
    rl = [porter.stem(wnl.lemmatize(i)) for i in rl if i not in sw]
    rl = [i for i in rl if i != ""]
    dict[count] = nltk.FreqDist(rl).items()
#    print count,dict[count]
    for w in dict[count]:
        if w[0] not in term_list:
            term_list.append(w[0])
print len(term_list)       
