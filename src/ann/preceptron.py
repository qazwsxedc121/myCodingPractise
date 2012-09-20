'''
Created on 2012-5-17

@author: guoxc
'''
import math
class preceptron_unit(object):
    def __init__(self,w0,weight,learning_rate = 0.1):
        self.w0 = w0
        self.weight = weight
        self.learning_rate = learning_rate
    def output(self,x):
        if(len(x) != len(self.weight)):
            return None
        if(sum([x[i]*self.weight[i] for i in range(len(x))]) + self.w0 > 0 ):
            return 1
        else:
            return 0
    def train(self,x,target):
        if(len(x) != len(self.weight)):
            return None
        delta = (target - self.output(x)) * self.learning_rate
        for i in range(len(x)):
            self.weight[i] += delta * x[i]
        self.w0 += delta 
        self.learning_rate *= 0.9
    def print_self(self):
        print self.w0, self.weight
        

class linear_unit(object):
    def __init__(self,w0,weight,learning_rate = 0.1):
        self.w0 = w0
        self.weight = weight
        self.learning_rate = learning_rate
    def output(self,x):
        if(len(x) != len(self.weight)):
            return None
        return sum([x[i]*self.weight[i] for i in range(len(x))]) + self.w0
    def train(self,x,target):
        if(len(x) != len(self.weight)):
            return None
        delta = (target - self.output(x)) * self.learning_rate
        for i in range(len(x)):
            self.weight[i] += delta * x[i]
        self.w0 += delta 
        self.learning_rate *= 0.9
    def print_self(self):
        print self.w0, self.weight
        




def test_main():
    u1 = linear_unit(-0.8, [0.5, 0.5])
    print u1.output([1,-1])
    for i in range(10):
        u1.train([1,-1], 1)
        u1.train([-1,1], 1)
        u1.train([1,1],1)
        u1.train([-1,-1],-1)
        u1.print_self()
    print u1.output([1,1]),u1.w0,u1.weight
if __name__ == "__main__":
    test_main()
#    po = [1,2,3]
#    po[2] += 2
#    print po