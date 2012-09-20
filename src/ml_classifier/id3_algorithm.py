'''
Created on 2012-6-7

@author: guoxc
'''
import classifier_trainset
import information_theory.entropy as entropy
class Node(object):
    def __init__(self, tag=None, branch=None, attr=None):
        self.tag_of_node = tag
        self.attr = attr
        self.branch = branch
def tree_print(node, layer=0):
    if not node:
        return
    if node.tag_of_node:
        print "|   " * (layer - 1 if layer >1 else 0) + "|___" * (1 if layer >= 1 else 0) + str(node.tag_of_node)
    if node.branch:
        if node.attr:
            print "|   " * layer + str(node.attr)
        for item in node.branch:
            tree_print(item, layer+1)
def get_entropy(train_set, target_attribute):
    t = [0 for i in range(target_attribute)]
    for i in train_set:
        t[i[-1]] += 1
    t = [1.0 * i / len(train_set) for i in t]
#    print t
    x = entropy.calc_entropy_bit(t)
#    print x
    return x

def subset_with_value(train_set, attribute, value):
    return [i for i in train_set if i[attribute] == value]

def choose_attr(train_set, target_attribute, attributes):
    entropy_s = get_entropy(train_set, target_attribute)
    gain = [0 for i in attributes]
    for i,j in enumerate(attributes):
        if j != 0:
            gain[i] = entropy_s
            for k in range(j):
                subset_k = subset_with_value(train_set, i, k)
                gain[i] -= 1.0 * len(subset_k) / len(train_set) * get_entropy(subset_k, target_attribute)
    return gain.index(max(gain))
def id3_tree_build(train_set, target_attribute, attributes):
    tag_of_node = train_set[0][-1] 
    for item in train_set :
        if item[-1] != tag_of_node:
            break
    else:
        return Node(tag_of_node)
    for item in attributes:
        if item != 0:
            break
    else:
        ic = [0 for i in range(target_attribute)]
        for j in train_set:
            ic[j[-1]] += 1
        return Node(ic.index(max(ic)))
    node = Node()
    node.branch = []
    ca = choose_attr(train_set, target_attribute, attributes)
    node.attr = ca
    for k in range(attributes[ca]):
        subset_k = subset_with_value(train_set, ca, k)
        if subset_k == []:
            ic = [0 for i in range(target_attribute)]
            for j in train_set:
                ic[j[-1]] += 1
            node.branch.append(Node(ic.index(max(ic))))
        else:
            node.branch.append(id3_tree_build(subset_k, target_attribute, attributes[:ca]+[0,]+attributes[ca+1:]))
    return node

def formalize_trainset(train_set, target_attr, attr):
    """formalize_trainset to int values"""
    train_set_re = []
    for item in train_set:
        train_set_re.append([attr[i][1].index(j) for i,j in enumerate(item[0])] +
                            [target_attr.index(item[1]),])
#    print train_set_re
    attr_re = [len(item[1]) for item in attr]
    return train_set_re, len(target_attr), attr_re

def main():
    tags,attrs,train_set = classifier_trainset.get_trainset("car")
    attrs_dict = {}
    for item in attrs:
        attrs_dict[item[0]] = item[1]
    train_set, tags, attrs = formalize_trainset(train_set, tags, attrs)
    root = id3_tree_build(train_set, tags, attrs)
    tree_print(root)
    
if __name__ == "__main__":
    main()