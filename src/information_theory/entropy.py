'''
Created on 2012-5-14

@author: guoxc
'''
import math
import unittest
def calc_entropy_bit(probabilities):
    return -math.fsum([p*math.log(p,2) for p in probabilities if p != 0.0])
class test_main(unittest.TestCase):
    def setUp(self):
        pass
    def test_calc_entropy_bit(self):
        self.assertEquals(calc_entropy_bit([0.5,0.5]),1.0)
        self.assertAlmostEquals(calc_entropy_bit([1.0/26 for i in range(0,26)]), 4.7, delta=0.1)
        print "entropy of [0.9,0.1]:   " + str(calc_entropy_bit([0.9,0.1]))
    def tearDown(self):
        pass
if __name__ == "__main__":
    unittest.main()

