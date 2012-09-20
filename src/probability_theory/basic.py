'''
Created on 2012-5-21

@author: guoxc
'''
import Bernoulli_distribution
import math
THRESHOLD = 0.000000001
class RandomVar(object):
    ''' a random variable of 1 demention'''
    def __init__(self, value = None, distribution = None):
        if value == None:
            self.value = [0,]
        else:
            self.value = value
        if distribution == None:
            self.distribution = [1,]
        else:
            self.distribution = distribution
        if not self._check_init():
            assert False
            
    def _check_init(self):
        """check if the RandomVar legal and normalize the distribution"""
        if len(self.value) != len(self.distribution):
            return False
        temp = sum(self.distribution)
        for i in range(len(self.value)):
            self.distribution[i] /= temp
        return True
    
    def expaction(self, func=None):
        if func is None:
            func = lambda x:x
        return sum([1.0 * func(self.value[i]) * self.distribution[i] 
                    for i in range(len(self.value))])
        
    def k_order_central_moment(self, k):
        expaction_x = self.expaction()
        new_var = RandomVar([(i - expaction_x) ** k 
                        for i in self.value], self.distribution)
        return new_var.expaction()
    
    def variance(self):
        return self.k_order_central_moment(2)
    
    def random_deviation(self):
        expaction_x = self.expaction()
        varianve_x = self.variance()
        sqrt_varianve_x = math.sqrt(varianve_x)
        return RandomVar([(var_x - expaction_x) / sqrt_varianve_x 
                          for var_x in self.value], self.distribution)
    
class RandomVar_2(object):
    ''' a random variable of 2 demention'''
    def __init__(self, value=None, distribution=None, valuex=None, valuey=None):
        if value is None:
            self.valuex = valuex
            self.valuey = valuey
        else:
            self.valuex = value[0]
            self.valuey = value[1]
        self.distribution = distribution
        if not self._check_init():
            assert False
            
    def _check_init(self):
        """check if the RandomVar_2 legal and normalize the distribution"""
        if len(self.valuex) != len(self.distribution[0]):
            return False
        if len(self.valuey) != len(self.distribution):
            return False
        temp = sum([sum(i) for i in self.distribution])
        for i in range(len(self.valuex)):
            for j in range(len(self.valuey)):
                self.distribution[j][i] /= temp
        return True 
    
    def distribution_x(self):
        seq_plus = lambda x,y:[x[i]+y[i] for i in range(min(len(x), len(y)))]
        return reduce(seq_plus, self.distribution)
    
    def distribution_y(self):
        return [sum(i) for i in self.distribution]
    
    def expaction_x(self,func=None):
        if func is None:
            func = lambda x:x
        dis_x = self.distribution_x()
        return sum([1.0 * func(self.valuex[i]) * dis_x[i] for i in range(len(dis_x))])
    
    def expaction_y(self,func=None):
        if func is None:
            func = lambda x:x
        dis_y = self.distribution_y()
        return sum([1.0 * func(self.valuey[i]) * dis_y[i] for i in range(len(dis_y))])
    
    def expaction_xy(self,func=None):
        if func is None:
            func = lambda x, y:x * y
        return sum([sum([1.0 * func(self.valuex[i], self.valuey[j]) * self.distribution[j][i] 
                         for i in range(len(self.valuex))]) for j in range(len(self.valuey))])
        
    def expaction_xuy(self,y_index=0,func=None):
        if func is None:
            func = lambda x:x
        py = self.probability_y(y_index)
        dis_x = [self.distribution[y_index][i] / py for i in range(len(self.valuex))]
        return sum([1.0 * func(self.valuex[i]) * dis_x[i] for i in range(len(self.valuex))])
    
    def expaction_yux(self,x_index=0,func=None):
        if func is None:
            func = lambda x:x
        px = self.probability_x(x_index)
        dis_y = [self.distribution[i][x_index] / px for i in range(len(self.valuey))]
        return sum([1.0 * func(self.valuey[i]) * dis_y[i] for i in range(len(self.valuey))])
    
    def covariance(self):
        return self.expaction_xy() - self.expaction_x() * self.expaction_y()
    
    def probability_x(self,x_index):
        px = sum([self.distribution[i][x_index] for i in range(len(self.valuey))])
        return px
    
    def probability_y(self,y_index):
        py = sum(self.distribution[y_index])
        return py
    
    def idependent(self):
        for i in range(len(self.valuex)):
            for j in range(len(self.valuey)):
                if abs(self.distribution[j][i] - (self.probability_x(i) * self.probability_y(j))) >= THRESHOLD:
                    return False
        return True
    
if __name__ == "__main__":
    VAR_X = RandomVar([1, 2, 3, 4], [0.25, 0.1, 0.4, 0.25])
    print VAR_X.expaction()
    print VAR_X.variance()
    VAR_X = RandomVar(range(-5, 6), 
                      Bernoulli_distribution.b_distribution(10, 0.5))
    print VAR_X.expaction()
    print VAR_X.variance()
    ERROR = VAR_X.random_deviation()
    print ERROR
    print ERROR.expaction(), ERROR.variance()
    VAR_2 = RandomVar_2([[1, 2, 3, 4], [2, 1, 2]], 
                        [[0.02, 0.08, 0.04, 0.06], 
                         [0.03, 0.12, 0.06, 0.09], 
                         [0.05, 0.20, 0.10, 0.15]])
    print VAR_2.distribution_x()
    print VAR_2.expaction_x()
    print VAR_2.expaction_y()
    print VAR_2.expaction_xy()
    print VAR_2.expaction_xuy(1)
    print VAR_2.idependent()