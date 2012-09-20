'''
Created on 2012-5-30

@author: guoxc
'''
import cPickle
import csv
import math
data_file = open("../../data/article_data.dat","r")
data_dict = cPickle.load(data_file)

def zip_data_dict(i):
    word_l = []
    time_l = []
    for word,time in data_dict[i]:
        word_l.append(word)
        time_l.append(time)
    return word_l,time_l

person_dict = {}
for i in range(1,5552):
    person_dict[i] = []
train_file = open("../../data/user-info-train.csv","rb")
csv_reader = csv.reader(train_file)
for p,a in csv_reader:
    p = int(p)
    a = int(a)
    person_dict[p].append(a)

test_dict = {}
for i in range(1,5552):
    test_dict[i] = []
train_file = open("../../data/user-info-test.csv","rb")
csv_reader = csv.reader(train_file)
for p,a in csv_reader:
    p = int(p)
    a = int(a)
    test_dict[p].append(a)
    
sim_pairs = {}

def find_sim(person, article):
    if article in person_dict[person]:
        return 100000.0
    return sum([find_sim_paper(i,article) for i in person_dict[person]])
    
def find_sim_paper(paper1, paper2):
    if (paper1,paper2) in sim_pairs:
        return sim_pairs[(paper1,paper2)]
    paper1_wl,paper1_tl = zip_data_dict(paper1)
    paper2_wl,paper2_tl = zip_data_dict(paper2)
    result = 1.0
    for i in range(len(paper2_wl)):
        if paper2_wl[i] in paper1_wl:
            result *= math.exp(paper1_tl[paper1_wl.index(paper2_wl[i])] * 1.0 / sum(paper1_tl)) ** paper2_tl[i]
    sim_pairs[(paper1,paper2)] = result
    return result

result_file = open("../../data/recommender_result.txt","w")
for j in range(1,5552):
    rlist = [(find_sim(j,i), i) for i in test_dict[j]]
    rlist.sort()
    rlist.reverse()
    rstr = str(j)+", "+str(rlist[0][1])+"; "+str(rlist[1][1])+"; "+str(rlist[2][1])+"; "+str(rlist[3][1])+"; "+str(rlist[4][1])+"\n"
    print rstr
    result_file.write(rstr)