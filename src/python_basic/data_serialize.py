'''
Created on 2012-5-17

@author: guoxc
'''
import cPickle
import unittest
def dump_cpickle():
    file1 = open("../../data/data1.dat","w")
    data = range(10)
    cPickle.dump(data, file1)
def load_cpickle():
    file2 = open("../../data/data1.dat","r")
    print cPickle.load(file2)

class TestMain(unittest.TestCase):
    def test_dump_cpickle(self):
        dump_cpickle()
    def test_load_cpickle(self):
        load_cpickle()
if __name__ == "__main__":
    unittest.main()