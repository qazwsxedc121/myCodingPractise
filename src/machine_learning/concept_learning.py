'''
Created on 2012-5-31

@author: guoxc
'''
train_data_set = [[2, 1, 0, 1, 1, 0, 1],
                  [2, 1, 1, 1, 1, 0, 1],
                  [0, 0, 1, 1, 1, 1, 0],
                  [2, 1, 1, 1, 0, 1, 1]]

and_opr = lambda x, y: x and y
or_opr = lambda x, y: x or y

def judge_model(train_entry, model):
    if len(train_entry) != len(model) + 1:
        return False
    result = [judge_code(train_entry[i], model[i]) for i in range(len(model))]
    judge = reduce(and_opr, result)
    return judge == (train_entry[-1] == 1)

def judge_code(code, model):
    if model == -1:
        return True
    elif model == -2:
        return False
    else:
        return model == code

def judge_set(train_set, model):
    result = [judge_model(i, model) for i in train_set]
    return reduce(and_opr, result)

def general_or_equal_code(code1, code2):
    if code1 == -1:
        return True
    elif code1 >= 0:
        if code2 == code1 or code2 == -2:
            return True 
        else:
            return False
    else:
        if code1 == code2:
            return True
        else:
            return False
    
def special_or_equal_code(code1, code2):
    if code1 == -2:
        return True
    elif code1 >= 0:
        if code2 == code1 or code2 == -1:
            return True
        else:
            return False
    else:
        if code1 == code2:
            return True
        else:
            return False
    
def general_code(code1, code2):
    if code1 == -1:
        if code2 != -1:
            return True
        return False
    elif code1 >= 0:
        if code2 == -2:
            return True
        return False
    else:
        return False

def special_code(code1, code2):
    if code1 == -2:
        if code2 != -2:
            return True
        return False
    elif code1 >= 0:
        if code2 == -1:
            return True
        return False
    else:
        return False   

def generalize_1step(model, train_entry=None, mxc=None):
    result = []
    if train_entry == None:
        for i in range(len(model)):
            if model[i] == -1:
                continue
            for j in generalize_1step_code(model[i], maxchoice=mxc[i]):
                model_f = model[:i] + [j, ] + model[i + 1:]
                result.append(model_f)
    elif not judge_model(train_entry, model):
        model_f = [i for i in model]
        for i in range(len(model)):
            g_code = generalize_1step_code(model[i], train_code=train_entry[i],maxchoice=mxc[i]).next()
            model_f[i] = g_code
        result.append(model_f)
    else:
        result += generalize_1step(model, mxc=mxc)
    return result
    
def specialize_1step(model, train_entry=None, mxc=None):
    result = []
    if train_entry == None:
        for i in range(len(model)):
            if model[i] == -2:
                continue
            for j in specialize_1step_code(model[i], maxchoice=mxc[i]):
                model_f = model[:i] + [j, ] + model[i + 1:]
                result.append(model_f)
    elif not judge_model(train_entry, model):
        for i in range(len(model)):
            for g_code in specialize_1step_code(model[i], train_code=train_entry[i],maxchoice=mxc[i]):
                model_f = model[:i]+[g_code,]+model[i+1:]
                result.append(model_f)
    else:
        result += specialize_1step(model, mxc=mxc)
    return result   

def generalize_1step_code(code, train_code=None, maxchoice=2):
    if train_code != None:
        if code == -2 or code == train_code:
            yield train_code
        else:
            yield -1
    elif code == -1 or code >= 0:
        yield -1
    else:
        for i in range(maxchoice):
            yield i
            
def specialize_1step_code(code, train_code=None, maxchoice=2):
    if train_code != None:
        if code == -1 :
            for i in range(maxchoice):
                if i != train_code:
                    yield i
        else:
            yield -2
    elif code == -2 or code >= 0:
        yield -2
    else:
        for i in range(maxchoice):
            yield i   
    
def more_general_than(model1, model2):
    if more_general_or_equal(model1, model2) and model1 != model2:
        return True
    return False
    
def more_general_or_equal(model1, model2):
    if len(model1) != len(model2):
        return False
    result = [general_or_equal_code(model1[i], model2[i]) for i in range(len(model1))]
    return reduce(and_opr, result)
    
def more_special_than(model1, model2):
    if more_special_or_equal(model1, model2) and model1 != model2:
        return True
    return False
    
def more_special_or_equal(model1, model2):
    if len(model1) != len(model2):
        return False
    result = [special_or_equal_code(model1[i], model2[i]) for i in range(len(model1))]
    return reduce(and_opr, result)

def find_s_and_g(train_set, maxchoice=None):
    length = len(train_set[0]) - 1
    g = [[-1 for i in range(length)]]
    s = [[-2 for i in range(length)]]
    for i in train_set:
        if i[-1] == 0:
            s = [item for item in s if judge_model(i, item)]
            addlist = []
            for item in g:
                if not judge_model(i, item):
                    g.remove(item)
                    slist = specialize_1step(item, i, mxc=maxchoice)
                    for to_be_added in slist:
                        tf_list = [more_special_than(gitem, to_be_added)
                                   for gitem in s]
                        if (len(tf_list) > 1 and reduce(or_opr, tf_list)) or (len(tf_list) == 1 and tf_list[0]):
                            addlist.append(to_be_added)
            g += addlist
            for item1 in g:
                for item2 in g:
                    if item1 == item2 : continue
                    if more_special_than(item2, item1):
                        g.remove(item2)
        else:
            g = [item for item in g if judge_model(i, item)]
            addlist = []
            for item in s:
                if not judge_model(i, item):
                    s.remove(item)
                    glist = generalize_1step(item, i, mxc=maxchoice)
                    for to_be_added in glist:
                        tf_list = [more_general_than(gitem, to_be_added)
                                   for gitem in g]
                        if (len(tf_list) > 1 and reduce(or_opr, tf_list)) or (len(tf_list) == 1 and tf_list[0]):
                            addlist.append(to_be_added)
            s += addlist
            for item1 in s:
                for item2 in s:
                    if item1 == item2 : continue
                    if more_general_than(item2, item1):
                        s.remove(item2)
    print g, s 

assert judge_set(train_data_set, [2] + [-1] * 5)
assert more_general_or_equal([-1] * 5, [2] + [-1] * 4)
assert not more_general_or_equal([2] + [-1] * 5, [-1] * 6)
assert more_general_than([-1] * 5, [2] + [-1] * 4)
assert not more_general_than([-1] * 5, [-1] * 5)
find_s_and_g(train_data_set, maxchoice=[3,2,2,2,2,2])
dw1 = generalize_1step([-2, -2, -2], train_entry=[0, 1, 0, 1],mxc=[2] * 3)
dw2 = generalize_1step(dw1[0], train_entry=[0, 1, 0, 1],mxc=[2] * 3)
dw3 = generalize_1step(dw2[0], train_entry=[0, 1, 1, 1],mxc=[2] * 3)
dw4 = generalize_1step(dw3[0], train_entry=[0, 1, 0, 1],mxc=[2] * 3)
print dw1, dw2, dw3, dw4
print generalize_1step([-2, -2, -2], mxc=[2, 2, 2])
