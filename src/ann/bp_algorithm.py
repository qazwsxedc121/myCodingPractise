'''
Created on 2012-5-14

@author: guoxc
'''
#
import math
import unittest
class simple_2layer_network(object):
    def __init__(self,unit1, unit2, unit3, unit4):
        self.unit1 = unit1
        self.unit2 = unit2
        self.unit3 = unit3
        self.unit4 = unit4
        self.layer1 = [self.unit1, self.unit2]
        self.layer2 = [self.unit3, self.unit4]
    
    def output(self,x):
        return self.layer2_output(x)
        
    def layer2_output(self,x):
        return [i.output(self.layer1_output(x)) for i in self.layer2]
    
    def layer1_output(self,x):
        return [self.layer1[j].output(x[j]) for j in range(len(self.layer1))]

    def train(self,x,target):
        layer2_output = self.layer2_output(x)
        layer1_output = self.layer1_output(x)
#        unit2_output = self.unit2.output(x[1])
        delta_k = lambda uo,ta:uo * (1 - uo) * (ta - uo)
        delta_h = lambda uo,ly2,j,dl2:uo * (1 - uo) * sum([ly2[i].weight[j] * dl2[i] for i in range(len(ly2))])
        delta_layer2 = [delta_k(layer2_output[i],target[i]) for i in range(len(self.layer2))]
        delta_layer1 = [delta_h(layer1_output[i],self.layer2,i,delta_layer2) for i in range(len(self.layer1))]
#        delta_2 = unit2_output * (1 - unit2_output) * (self.unit3.weight[1] * delta_3 + self.unit4.weight[1] * delta_4)
        for i in range(len(self.layer1)):
            self.layer1[i].config_with_delta_weight([delta_layer1[i] * x[j] * self.layer1[i].learning_rate for j in range(len(self.layer1[i].weight))])
            for j in range(len(self.layer1[i].weight)):
                self.layer1[i].weight[j] += delta_layer1[i] * x[j] * self.layer1[i].learning_rate
        for i in range(len(self.layer2)):
            for j in range(len(self.layer2[i].weight)):
                self.layer2[i].weight[j] += delta_layer2[i] * layer1_output[j] * self.layer2[i].learning_rate
        
#        self.unit1.weight[0] += delta_1 * x[0][0] * self.unit1.learning_rate
#        self.unit4.weight[0] += delta_4 * unit1_output * self.unit4.learning_rate
        

class sigmoid_unit(object):
    def __init__(self,w0,weight,learning_rate = 0.1):
        self.w0 = w0
        self.weight = weight
        self.learning_rate = learning_rate
    def output(self,x):
        if(len(x) != len(self.weight)):
            return None
        return sigmoid(sum([x[i]*self.weight[i] for i in range(len(x))]) + self.w0)
    def train(self,x,target):
        if(len(x) != len(self.weight)):
            return None
        delta = (target - self.output(x)) * self.learning_rate
        for i in range(len(x)):
            self.weight[i] += delta * x[i]
#        self.w0 += delta 
#        self.learning_rate *= 0.9
    def config_with_delta_weight(self,deltaweight):
        for i in range(len(self.weight)):
            self.weight[i] += deltaweight[i]
            
    def print_self(self):
        print self.w0, self.weight
        

def sigmoid(y):
    return 1.0 / (1 + math.exp(-y))

class test_main(unittest.TestCase):
    def setUp(self):
        unit1 = sigmoid_unit(0,[-0.02,])
        unit2 = sigmoid_unit(0,[0.03,])
        unit3 = sigmoid_unit(0,[0.01,-0.02])
        unit4 = sigmoid_unit(0,[-0.02,0.01])
        self.sn = simple_2layer_network(unit1,unit2,unit3,unit4)
    def testBp(self):
        for i in range(100):
            self.sn.train([[1,],[1,]], [-1,-1])
        print self.sn.output([[1,],[1,]])
    
    def testSigmoid(self):
        unit1 = sigmoid_unit(0,[-0.02,])
        for i in range(1000):
            unit1.train([1,], 0)
            unit1.train([-1,],1)
#            unit1.print_self()
        print unit1.output([1,])
        print unit1.output([-1,])
        print unit1.output([-0.5,])
        unit1.print_self()

if __name__ == "__main__":
    unittest.main()