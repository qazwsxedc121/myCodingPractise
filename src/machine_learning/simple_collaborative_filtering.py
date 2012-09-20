'''
Created on 2012-5-24

@author: guoxc
'''
import cPickle
import math
DATA_FILE = open("../../data/recommendation.dat","r")
CRITICS = cPickle.load(DATA_FILE)
print CRITICS
def sim_distance(prefs, person1, person2):
    """ distance """
    si_list = [item for item in prefs[person1] if item in prefs[person2]]
    if len(si_list) == 0:
        return 0
    sum_of_squares = sum([(prefs[person1][item] - prefs[person2][item])**2 for 
                          item in prefs[person1] if item in prefs[person2]])
    return 1 / (1 + math.sqrt(sum_of_squares))

def sim_pearson(prefs, person1, person2):
    """ pearson """
    si_list = [item for item in prefs[person1] if item in prefs[person2]]
    if len(si_list) == 0:
        return 1
    sum1 = sum([prefs[person1][it] for it in si_list])
    sum2 = sum([prefs[person2][it] for it in si_list])
    sum1_sq = sum([prefs[person1][it]**2 for it in si_list])
    sum2_sq = sum([prefs[person2][it]**2 for it in si_list])
    p_sum = sum([prefs[person1][it] * prefs[person2][it] for it in si_list])
    num = p_sum - (sum1 * sum2 / len(si_list))
    den = math.sqrt((sum1_sq - sum1**2 / len(si_list))
                    * (sum2_sq - sum2**2 / len(si_list)))
    if den == 0:
        return 0
    return num / den

def sim_tanimoto(prefs, person1, person2):
    si_list = [item for item in prefs[person1] if item in prefs[person2]]
    return len(si_list) / (len(prefs[person1]) 
                           + len(prefs[person2]) - len(si_list))

def top_matches(prefs, person, length=5, similarity=sim_pearson):
    """ return the persons with biggest similarity of this person """
    scores = [(similarity(prefs, person, other), other)
              for other in prefs if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:length]

def get_recommendations(prefs, person, similarity=sim_pearson):
    """make item recommendations for person """
    totals = {}
    sim_sums = {}
    for other in prefs:
        if other == person:
            continue
        sim = similarity(prefs, person, other)
        if sim <= 0:
            continue
        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item] == 0:
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                sim_sums.setdefault(item, 0)
                sim_sums[item] += sim
    rankings = [(total / sim_sums[item], item) 
                for item, total in totals.items()]
    rankings.sort()
    rankings.reverse()
    return rankings

def transform_prefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            result[item][person] = prefs[person][item]
    return result