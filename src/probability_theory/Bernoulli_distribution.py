'''
Created on 2012-5-15

@author: guoxc
'''
import unittest
import combinatorics.basic


def b_distribution(n,p):
    re = [combinatorics.basic.C(k,n)*(p**k)*((1-p)**(n-k)) for k in range(0,n+1)]
    return re


class tester(unittest.TestCase):
    def test_b_distribution(self):
        self.assertEqual(b_distribution(2, 0.5),[0.25,0.5,0.25])

if __name__ == "__main__":
    unittest.main()