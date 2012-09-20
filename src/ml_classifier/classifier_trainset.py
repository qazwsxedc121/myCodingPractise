'''
Created on 2012-6-7

@author: guoxc
'''
import re
set_str = "car"

def get_trainset(set_name="car"):
    """
    return a trainset (class,attribute,trainset)
    class -> ['the_tag_of_trainsets',..]
    attribute -> [('the_attributes_name',['the_range_of_attr',..),..]
    trainset -> [(['values_of_attr',..],'tag'),..]
    """
    names_file = open("../../data/"+set_str+"/"+set_name+"_names.dat", "r")
    data_file= open("../../data/"+set_str+"/"+set_name+"_data.dat", "r")
    
    names_strs = names_file.readlines()
    v_index = 0
    a_index = 0
    for index,line in enumerate(names_strs):
        if line.find("| class values") != -1:
            v_index = index
        elif line.find("| attributes") != -1:
            a_index = index
            break
    class_values_strs = re.split(r"\W+",names_strs[v_index+2].strip())
    attribute_namea_value_list = []
    for i in range(a_index, len(names_strs)):
        if re.search(r"^\w+:\s+[\w,\s]+\.",names_strs[i]) != None:
            temp_strs = re.split(r"\W+",names_strs[i][:-2])
            attribute_namea_value_list.append((temp_strs[0],temp_strs[1:]))
#    print class_values_strs
#    print attribute_namea_value_list
    train_set = []
    while True:
        temp_str = data_file.readline()[:-1]
        if temp_str == "":
            break
        values = temp_str.split(",")
        train_set.append((values[:-1], values[-1]))
    return class_values_strs,attribute_namea_value_list,train_set