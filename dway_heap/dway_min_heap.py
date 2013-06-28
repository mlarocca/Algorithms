from dway_heap import create_heap, empty, peek, size

def put(heap, new_item):
  ''' Insert a new element in the heap
      : param heap : A valid dway min-heap.
      : type heap : Heap, a pseudo-object created by dway_heap.create_heap function.
      : param new_item : The element to insert.
      : return : self, to allow method chaining.  
  '''
  try:
    queue = heap["queue"]
    d = heap["d"]
  except KeyError:
    raise TypeError("Invalid heap object")
  except TypeError:
    raise TypeError("Invalid heap object")  
    
  queue.append(new_item) #insert a placeholder to enlarge the array
  
  pos = len(queue) - 1
  parent = (pos - 1) / d
  
  while parent >= 0:
    
    if new_item < queue[parent]:
      
      queue[pos] = queue[parent]
      pos = parent
      parent = (parent - 1) / d        
    else:
      parent = pos
      break
    
  if parent < 0:
    parent = 0
      
  queue[parent] = new_item
  assert check(heap)
  return
  
def top(heap):
  ''' Returns the top element, and removes it from the heap.
      : param heap : A valid dway min-heap.
      : type heap : Heap, a pseudo-object created by dway_heap.create_heap function.
      : raise Exception : If the heap is empty.
      : return : The top element.
  '''
  try:
    queue = heap["queue"]
    d = heap["d"]
  except KeyError:
    raise TypeError("Invalid heap object")
  except TypeError:
    raise TypeError("Invalid heap object")
  

  #removes the last element from the queue
  try:
    item = queue.pop()
  except IndexError:
    raise IndexError("top of an empty queue")
  
  size = len(queue)
  
  if size == 0:
    return item
  else:
    res = queue[0]
    
    pos = 0
    tmp_pos = pos * d + 1
    child_pos = tmp_pos  
        
    while child_pos < size:
      #Look for the smallest children
      i = 1
      while i < d and tmp_pos + i < size:
        if queue[tmp_pos + i] < queue[child_pos]:
          child_pos = tmp_pos + i 
        i += 1
      if queue[child_pos] < item:
        queue[pos] = queue[child_pos]
        
        pos = child_pos
        tmp_pos = pos * d + 1
        child_pos = tmp_pos
      else:
        break
      
    queue[pos] = item
    
    assert check(heap)
    return res
 
def decrease_priority(heap, old_element, new_element):
  ''' Decrease the priority of a given key
      WARNING: duplicates keys aren't handled!
      : param heap : A valid dway min-heap.
      : type heap : Heap, a pseudo-object created by dway_heap.create_heap function.
      : param old_element : The element to be replaced.
      : param new_element : The new value for that element. 
      : raise IllegalArgumentException : If the new element is greater than the the existing one.
      : return : True iff the old element was in the heap and it is successfully updated.
  '''    
  if new_element > old_element:
    raise Exception("In min-heaps existing elements' priority can only be decreased!") 
  
  try:
    queue = heap["queue"]
    d = heap["d"]
  except KeyError:
    raise TypeError("Invalid heap object")
  except TypeError:
    raise TypeError("Invalid heap object")
  
    
  size = len(queue)

  for pos in xrange(size):
    item = queue[pos]
    if item == old_element:
      queue[pos] = new_element
      break
  if pos == size:
    return False  #Key not found
  
  parent = (pos - 1) / d
  
  while parent >= 0:
    
    if new_element < queue[parent]:
      
      queue[pos] = queue[parent]
      pos = parent
      parent = (parent - 1) / d        
    else:
      parent = pos
      break
    
  if parent < 0:
    parent = 0
  queue[parent] = new_element 
  
  assert check(heap) 

def heapsort(heap):
  ''' Return a sorted array with all the elements in the heap.
      WARNING: All the elemens will be removed from the heap!
      : param heap : A valid dway min-heap.
      : type heap : Heap, a pseudo-object created by dway_heap.create_heap function.
      : return : An array with the elements in the heap.
  '''
  
  if empty(heap):
    return []
  else:
    try:
      queue = heap["queue"]
    except KeyError:
      raise KeyError("Invalid heap object")
  
    res = []
    while len(queue) > 0:
      res.append(top(heap))
    
    return res

        
def check(heap):
  ''' Check queue integrity
      : param heap : A valid dway min-heap.
      : type heap : Heap, a pseudo-object created by dway_heap.create_heap function.
      : raise AssertionError : If the main property of the dway heap is violated
      : return : True iff the heap is valid
  '''
  try:
    queue = heap["queue"]
    d = heap["d"]
  except KeyError:
    raise TypeError("Invalid heap object")
  except TypeError:
    raise TypeError("Invalid heap object")
  
  pos = 0
  child = 1
  size = len(queue)
  while child < size:
    i = 0
    while i < d and child + i < size:
      assert queue[child + i] >= queue[pos]
      i += 1
      
    pos += 1
    child = pos * d + 1
  
  return True

