'''
Created on 08/apr/2013

@author: mlarocca
'''


class dway_heap(object):
  
  PRIORITY_INDEX = 0
  ELEMENT_INDEX = 1
  
  def __init__(self, d, max_heap=False):
    ''' : Constructor :
        Create a new d-way heap priority queue.
        : param d : The branch-factor of the heap.
                    (MUST be at least 2)
        : type d : int (Other types will be converted to int)
        : param max_heap : If passed and truthy, the heap will 
                            be a max heap instead than a min heap.
        : type max_heap : boolean 
        : raise IllegalArgumentException : If d is less than 2.
        : return : self, as all constructors.
    '''
    self.__d = int(d)
    
    if self.__d < 2:
      raise Exception("IllegalArgumentException: minimum allowed branch-factor is 2")
    
    #if it is a max queue, uses the reverse ordering
    #The function projects the 
    self.__smaller = ((lambda x, y: x[dway_heap.PRIORITY_INDEX] > 
                                    y[dway_heap.PRIORITY_INDEX]) 
                      if max_heap 
                      else (lambda x, y: x[dway_heap.PRIORITY_INDEX] < 
                                         y[dway_heap.PRIORITY_INDEX])
                     )
    #same function, but without the need to project the priority the tuple
    self.__smaller_priority = ((lambda x, y: x > y) if max_heap 
                                else (lambda x, y: x < y))
    
    self.__queue = []

  def empty(self):
    ''' Shortcut for heap.size() == 0
        : return : True <=> there is no element in the heap
    '''    
    return len(self.__queue) <= 0
  
  def size(self):
    ''' Return the number of elements in the heap
        : return : The number of elements in the heap
    '''
    return len(self.__queue)

  def put(self, element, priority):
    ''' Insert a new element in the heap
        : param element : The element to insert.
        : param priority : The priority associated with the element.
        : return : self, to allow method chaining.
        
    '''
    new_item = (priority, element)
    self.__queue.append(new_item) #insert a placeholder to enlarge the array
    
    pos = len(self.__queue) - 1
    parent = (pos - 1) / self.__d
    
    while parent >= 0:
      
      if self.__smaller(new_item, self.__queue[parent]):
        
        self.__queue[pos] = self.__queue[parent]
        pos = parent
        parent = (parent - 1) / self.__d        
      else:
        parent = pos
        break
      
    if parent < 0:
      parent = 0
      
    self.__queue[parent] = new_item     
    assert self.check()
    
    return self
  
  def top(self):
    ''' Returns the top element, and removes it from the heap.
        
        : raise Exception : If the heap is empty.
        : return : The top element.
    '''
    size = self.size()
    if size == 0:
      raise Exception("The Heap is empty")
    
    #removes the last element from the queue
    item = self.__queue.pop()
    size -= 1
    
    if size == 0:
      return item[dway_heap.ELEMENT_INDEX]
    else:
      res = self.__queue[0]
      
      pos = 0
      tmp_pos = pos * self.__d + 1
      child_pos = tmp_pos  
          
      while child_pos < size:
        #Look for the smallest children
        i = 1
        while i < self.__d and tmp_pos + i < size:
          if self.__smaller(self.__queue[tmp_pos + i], self.__queue[child_pos]):
            child_pos = tmp_pos + i 
          i += 1
        if self.__smaller(self.__queue[child_pos], item):
          self.__queue[pos] = self.__queue[child_pos]
          
          pos = child_pos
          tmp_pos = pos * self.__d + 1
          child_pos = tmp_pos
        else:
          break
        
      self.__queue[pos] = item
      
      assert self.check()
      return res[dway_heap.ELEMENT_INDEX]
 
  def decrease_priority(self, element, priority):
    ''' Decrease the priority of a given key
        WARNING: duplicates keys aren't handled!
        : param element : The "key", aka the element whose priority must be 
                          decreased.
        : param priority : The new priority for the element. 
        : raise IllegalArgumentException : If the new priority for a key is 
                                           greater than the the existing one.
        : return : True iff the key was in the heap and its priority 
                   has been successfully updated.
    '''    
    for pos in xrange(self.size()):
      item = self.__queue[pos]
      if item[dway_heap.ELEMENT_INDEX] == element:
        if not self.__smaller_priority(priority, item[dway_heap.PRIORITY_INDEX]):
          raise Exception("Existing key priority can only be decreased!") 
        self.__queue[pos] = new_item = (priority, element)
        break
    if pos == self.size():
      return False  #Key not found
    
    parent = (pos - 1) / self.__d
    
    while parent >= 0:
      
      if self.__smaller(new_item, self.__queue[parent]):
        
        self.__queue[pos] = self.__queue[parent]
        pos = parent
        parent = (parent - 1) / self.__d        
      else:
        parent = pos
        break
      
    if parent < 0:
      parent = 0
    self.__queue[parent] = new_item 
    
    assert self.check()
    
  def check(self):
    ''' Check queue integrity
        : raise AssertionError : If the main property of the dway heap is violated
        : return : True iff the heap is valid
    '''
    pos = 0
    child = 1
    
    while child < self.size():
      i = 0
      while i < self.__d and child + i < self.size():
        assert not self.__smaller(self.__queue[child + i], self.__queue[pos])
        i += 1
        
      pos += 1
      child = pos * self.__d + 1
    
    return True
    
  def clear(self):
    ''' Remove all the elements in the heap.
        : return : self, to allow method chaining.
    '''
    self.__queue = []
    return self
    
  def heapsort(self):
    ''' Return a sorted array with all the elements in the heap.
        WARNING: All the elemens will be removed from the heap!
        
        : return : An array with the elements in the heap.
    '''
    if self.empty():
      return []
    else:
      res = []
      while not self.empty():
        res.append( self.top())
      
      return res
    
    
  def __str__(self):
    ''' : override :
    '''
    return " ".join(map(lambda x : str(x[dway_heap.ELEMENT_INDEX]), self.__queue))

    
if __name__ == '__main__':
  
  from random import randrange
  
  def test():
    ''' Test the data structure
    '''
    print "Test min heap"
    
    for d in xrange(2,10):
      #Test d way
      print d
      pq = dway_heap(d)
      
      assert pq.empty()
      for i in xrange(d ** randrange(2, 4) + randrange(d)):
        k = randrange(1000000)
        pq.put(k, k)
        #Test insert
        assert not pq.empty()
        assert pq.size() == i + 1
      
      print "---------------"
      A = pq.heapsort()
  
      #check that A is sorted (i.e. elements are popped from the queue in the right order
      B = sorted(A)
      assert(B == A)
    
    print "Decrease key in min heap"  
    #Check decrease_key
    for d in xrange(2,10):
      #Test d way
      print d
      pq = dway_heap(d)
      memo = {}
      assert pq.empty()
      for i in xrange(d ** randrange(2, 4) + randrange(d)):
        k = randrange(1000000)
        pq.put(k,k)
        memo[(k, k)] = 1
        #Test insert
        assert not pq.empty()
        assert pq.size() == i + 1
      memo = memo.keys()
      for _ in xrange(min(5, randrange(pq.size()))):
        index = randrange(len(memo))
        item = memo.pop(index)
        pq.decrease_priority(item[dway_heap.ELEMENT_INDEX], item[dway_heap.PRIORITY_INDEX] / 2)
        item = (item[dway_heap.PRIORITY_INDEX] / 2, item[dway_heap.ELEMENT_INDEX])
        memo.append(item)  
          
    print "Test max heap"
    for d in xrange(2,10):
      #Test d way
      print d
      pq = dway_heap(d, True)
      
      assert pq.empty()
      for i in xrange(d ** randrange(2, 4) + randrange(d)):
        k = randrange(1000000)
        pq.put(k, k)
        #Test insert
        assert not pq.empty()
        assert pq.size() == i + 1
      
      print "---------------"
      A = pq.heapsort()
  
      #check that A is sorted (i.e. elements are popped from the queue in the right order
      B = sorted(A, reverse=True)
      assert(B == A)
        
    print "Decrease key in max heap"  
    #Check decrease_key
    for d in xrange(2,10):
      #Test d way
      print d
      pq = dway_heap(d, True)
      memo = {}
      assert pq.empty()
      for i in xrange(d ** randrange(2, 4) + randrange(d)):
        k = randrange(1000000)
        pq.put(k,k)
        memo[(k, k)] = 1
        #Test insert
        assert not pq.empty()
        assert pq.size() == i + 1
      memo = memo.keys()
      for _ in xrange(min(5, randrange(pq.size()))):
        index = randrange(len(memo))
        item = memo.pop(index)
        pq.decrease_priority(item[dway_heap.ELEMENT_INDEX], item[dway_heap.PRIORITY_INDEX] * 2)
        item = (item[dway_heap.PRIORITY_INDEX] * 2, item[dway_heap.ELEMENT_INDEX])
        memo.append(item)      
      
    print "Test OK"   
  #END of test definition  
    
  test()