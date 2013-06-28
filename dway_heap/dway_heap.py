'''
Created on 28/giu/2013

@author: mlarocca
'''
def empty(heap):
  ''' Shortcut for size(queue) == 0
      : param heap : A valid dway min-heap.
      : return : True <=> there is no element in the heap
  '''
  try:
    queue = heap["queue"]
  except KeyError:
    raise TypeError("Invalid heap object")
  except TypeError:
    raise TypeError("Invalid heap object")
    
  return len(queue) <= 0
  
  
def size(heap):
  ''' Return the number of elements in the heap
      : param heap : A valid dway min-heap.
      : return : The number of elements in the heap
  '''
  try:
    queue = heap["queue"]
  except KeyError:
    raise TypeError("Invalid heap object")
  except TypeError:
    raise TypeError("Invalid heap object")
  return len(queue)
  
    
def peek(heap):
  ''' Returns the top element, WITHOUT removing it from the heap.
      : param heap : A valid dway min-heap.
      : raise Exception : If the heap is empty.
      : return : The top element.
  '''  
  try:
    queue = heap["queue"]
  except KeyError:
    raise TypeError("Invalid heap object")
  except TypeError:
    raise TypeError("Invalid heap object")
  
  try:
    return queue[0]
  except IndexError:
    raise IndexError("peek on an empty queue")  

def create_heap(d):
  ''' : Constructor :
      Create a new d-way heap priority queue.
      : param d : The branch-factor of the heap.
                  (MUST be at least 2)
      : type d : int (Other types will be converted to int)
      : raise IllegalArgumentException : If d is less than 2.
      : return : A new dway-heap pseudo-object.
  '''  
  if d < 2:
    raise Exception("IllegalArgumentException: minimum allowed branch-factor is 2")  
  return {"d": d, "queue": []}