'''
Created on 2012-6-5

@author: guoxc
'''
import itertools

nl = ["1","2","3","4","5","6","7","8","9"]
al = ["A","B","C","D"]

#"""islice(seq,[start,],stop[,step])"""
for el in itertools.islice(nl,4):
    print el
print "\n"
for el in itertools.islice(nl,1,5):
    print el
print "\n"
for el in itertools.islice(nl,1,5,2):
    print el
print "\n"
    
nl = nl[:3]
al = al[:3]
#"""product(seq1,seq2,....[repeat=1])"""
for el in itertools.product(al,repeat=2):
    print el
print "\n"

for el in itertools.product(nl,al,al):
    print el
print "\n"
    
#"""permutations(p[,r])"""
for el in itertools.permutations(nl,2):
    print el
print "\n"

for el in itertools.permutations(nl):
    print el
print "\n"

#"""combinations(p,r)"""
print "itertools.combinations(nl,2)"
for el in itertools.combinations(nl,2):
    print el
print "\n"

#"""combinations_with_replacement(p,r)"""
print "itertools.combinations_with_replacement(nl,2)"
for el in itertools.combinations_with_replacement(nl,2):
    print el
print "\n"