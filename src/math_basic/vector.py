'''
Created on 2012-5-21

@author: guoxc
'''
import math
class Vector(list):
    @staticmethod
    def dot_product(vector1, vector2):
        if vector1._length != vector2._length:
            return None
        return sum([vector1.value[i] * vector2.value[i] for i in range(vector1._length)])
    
    @staticmethod
    def cross_product(vector1, vector2):
        if vector1._length != 3 or vector2._length != 3:
            return None
        vi = vector1.value[1] * vector2.value[2] - vector1.value[2] * vector2.value[1]
        vj = vector1.value[2] * vector2.value[0] - vector1.value[0] * vector2.value[2]
        vk = vector1.value[0] * vector2.value[1] - vector1.value[1] * vector2.value[0]
        return Vector([vi, vj, vk])
        
    def __init__(self,value = [0,0]):
        self.value = value
        self._length = len(value)
    def __len__(self):
        return self._length
    def __add__(self, other):
        if self._length != other:
            return None
        return Vector([self.value[i] + other.value[i] for i in range(self._length)])
    def __sub__(self, other):
        if self._length != other:
            return None
        return Vector([self.value[i] - other.value[i] for i in range(self._length)])
    def norm(self):
        return sum([i**2 for i in self.value])
    def to_list(self):
        return self.value
    