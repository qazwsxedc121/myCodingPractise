'''
Created on 2012-5-21

@author: guoxc
'''
import math
def p_distribution(lambda_, range_ = 10):
    re = [math.exp(-lambda_) * (lambda_ ** k) / math.factorial(k) for k in range(range_)]
    return re

if __name__ == "__main__":
    print p_distribution(0.8)