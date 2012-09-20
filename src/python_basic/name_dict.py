import cPickle
import random
dict_Original = open("../../data/SogouLabDic.txt","r").readlines()
list_normal = []
for line in dict_Original:
    line_split = line.split("\t")
    attribute = line_split[2].split(",")[:-1]
    list_normal.append((line_split[0],attribute))
dict_Now = open("../../data/SogouLabDicNew1.txt","w")
cPickle.dump(list_normal,dict_Now)
i = random.randrange(len(list_normal))
print list_normal[i]

