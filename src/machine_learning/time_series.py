'''
Created on 2012-5-28

@author: guoxc
'''
import math
import probability_theory.basic as pbasic

def minkowski_distance(list1, list2, p):
    if len(list1) != len(list2):
        return None
    return sum([math.fabs(list1[i] - list2[i]) ** p for i in range(len(list1))]) ** (1.0/p)


def test():
    print minkowski_distance([0,0], [1,1], 2)
    
def variance(list1):
    distribution = [1.0 / len(list1) for i in list1]
    list1_randomvar = pbasic.RandomVar(list1, distribution)
    return list1_randomvar.variance()

def mean(list1):
    return sum(list1) * 1.0 / len(list1)

def normalize(list1):
    std = math.sqrt(variance(list1))
    list_mean = mean(list1)
    return [(x - list_mean) / std for x in list1] 

def dtw(list1, list2, distance = None):
    if distance == None:
        distance = lambda x,y:(x - y) if x > y else (y - x)
    output = [[0 for i in list1+[0,]] for j in list2+[0,]]
    for i in range(1,len(list1)+1):
        output[0][i] = list1[i-1] 
    for j in range(1,len(list2)+1):
        output[j][0] = list2[j-1] 
    for i in range(1,len(list1)+1):
        for j in range(1,len(list2)+1):
            output[j][i] = min(output[j-1][i-1],output[j-1][i],output[j][i-1])+distance(list1[i-1],list2[j-1])
    for r in output:
        print r 

def plcs(list1,list2):
    b = [[0 for i in list1+["",]] for j in list2+["",]]
    c = [[0 for i in list1+["",]] for j in list2+["",]]
    for i in range(1,len(list1)+1):
        for j in range(1,len(list2)+1):
            if list1[i-1] == list2[j-1]:
                c[j][i] = c[j-1][i-1] + 1
                b[j][i] = 3
            elif c[j][i-1] >= c[j-1][i]:
                c[j][i] = c[j][i-1]
                b[j][i] = 1
            else:
                c[j][i] = c[j-1][i]
                b[j][i] = 2
    return c,b

def printlcs(list1,b,i,j):
    if i == 0 or j == 0:return []
    elif b[j][i] == 3:
        return printlcs(list1,b,i-1,j-1) +[list1[i-1],]
    elif b[j][i] == 1:
        return printlcs(list1,b,i-1,j)
    else:
        return printlcs(list1,b,i,j-1)
        
def lcs(list1,list2):
    c,b = plcs(list1,list2)
    print "length:" + str(c[len(list2)][len(list1)])
    print printlcs(list1,b,len(list1),len(list2))
    
#dtw([0,1,2,3,2,1,0,1,2],[0,1,1,2,2,3,1,0])
lcs([3,2,5,7,10,4,6],[2,5,4,7,3,10,8])