'''
Created on 2012-5-15

@author: guoxc
'''
import math
import unittest

#short for permutaion
def P(m,n):
    return permutation(m,n)

#short for combination
def C(m,n):
    return combination(m, n)


def permutation(m,n):
    return math.factorial(n)/math.factorial(n-m)


def combination(m,n):
    return math.factorial(n)/(math.factorial(n-m) * math.factorial(m))


class test_main(unittest.TestCase):

    def test_permutation(self):
        self.assertEquals(permutation(2,4),12)
        self.assertNotEqual(permutation(3,4), 1)
    
    def test_combination(self):
        self.assertEqual(combination(2, 4), 6)
        self.assertNotEqual(combination(3,4), 2)


if __name__ == "__main__":
    unittest.main()