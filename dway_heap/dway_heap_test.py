'''
Created on 28/giu/2013

@author: mlarocca
'''
import unittest
import dway_min_heap, dway_max_heap
from dway_heap import *
from random import randrange

class Test(unittest.TestCase):

  def test_min_heap(self):
    ''' Test the data structure
    '''
    print "Test min heap"
    
    for BRANCHING_FACTOR in xrange(2,10):
      #Test d way
      print BRANCHING_FACTOR
      pq = create_heap(BRANCHING_FACTOR)
      
      assert empty(pq)
      for i in xrange(BRANCHING_FACTOR ** randrange(2, 4) + randrange(BRANCHING_FACTOR)):
        k = randrange(1000000)
        dway_min_heap.put(pq, k)
        #Test insert
        assert not empty(pq)
        assert size(pq) == i + 1
      
      print "---------------"
      A = dway_min_heap.heapsort(pq)
  
      #check that A is sorted (i.e. elements are popped from the queue in the right order
      B = sorted(A)
      assert(B == A)
    
    print "Decrease key in min heap"  
    #Check decrease_key
    for BRANCHING_FACTOR in xrange(2,10):
      #Test d way
      print BRANCHING_FACTOR
      pq = create_heap(BRANCHING_FACTOR)
      memo = {}
      assert empty(pq)
      for i in xrange(BRANCHING_FACTOR ** randrange(2, 4) + randrange(BRANCHING_FACTOR)):
        k = randrange(1000000)
        dway_min_heap.put(pq,k)
        memo[k] = 1
        #Test insert
        assert not empty(pq)
        assert size(pq) == i + 1
      memo = memo.keys()
      for _ in xrange(min(5, randrange(size(pq)))):
        index = randrange(len(memo))
        item = memo.pop(index)
        dway_min_heap.decrease_priority(pq, item, item / 2)
        memo.append(item / 2)    

  def test_max_heap(self):
    ''' Test the data structure
    '''
    print "Test max heap"
    
    for BRANCHING_FACTOR in xrange(2,10):
      #Test d way
      print BRANCHING_FACTOR
      pq = create_heap(BRANCHING_FACTOR)
      
      assert empty(pq)
      for i in xrange(BRANCHING_FACTOR ** randrange(2, 4) + randrange(BRANCHING_FACTOR)):
        k = randrange(1000000)
        dway_max_heap.put(pq, k)
        #Test insert
        assert not empty(pq)
        assert size(pq) == i + 1
      
      print "---------------"
      A = dway_max_heap.heapsort(pq)
  
      #check that A is sorted (i.e. elements are popped from the queue in the right order
      B = sorted(A, reverse=True)
      assert(B == A)
    
    print "Decrease key in max heap"  
    #Check decrease_key
    for BRANCHING_FACTOR in xrange(2,10):
      #Test d way
      print BRANCHING_FACTOR
      pq = create_heap(BRANCHING_FACTOR)
      memo = {}
      assert empty(pq)
      for i in xrange(BRANCHING_FACTOR ** randrange(2, 4) + randrange(BRANCHING_FACTOR)):
        k = randrange(1000000)
        dway_max_heap.put(pq,k)
        memo[k] = 1
        #Test insert
        assert not empty(pq)
        assert size(pq) == i + 1
      memo = memo.keys()
      for _ in xrange(min(5, randrange(size(pq)))):
        index = randrange(len(memo))
        item = memo.pop(index)
        dway_max_heap.increase_priority(pq, item, item * 2)
        memo.append(item * 2)           
  #END of test definition  


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()