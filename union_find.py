'''
Created on 06/apr/2013

@author: mlarocca
'''

class UnionFind:
  
  def __init__(self, size):
    ''' : Constructor :
        Create a new union-find data structure
        : param size : The initial size of the union-find;
                       The size can be later increased, but not decreased.
        : type size : int (Other types will be converted to int)
        : raise IllegalArgumentException : If size is less than 1.
        : return : self, as all constructors.
    '''    
    self.n = int(size)
    if self.n <= 0:
      raise Exception("IllegalArgumentException: size must be positive")
    
    self.set = range(size)
    self.set_size = [1 for _ in xrange(size)]
    
  def add_element(self):
    ''' Add a new element to the union-find; the new element
        will be assigned to its own component.
        : return : self, to allow method chaining.
    '''
    self.set.append(self.n)
    self.set_size.append(1)
    self.n += 1
    return self
  
  def find_root(self, i):
    ''' 
        Implement find with path compression
        : param i : The element whose root has to be found.
        : type i : int (Other types will be converted to int)
    '''
    #makes sure i is an integer
    i = int(i)

    if self.set[i] != i:
      self.set[i] = self.find_root(self.set[i]) 
    
    return self.set[i]
  
    
  def connected(self, i, j):
    ''' Are elements i and j connected?
        : param i : The first element to check.
        : param j : The second element to check.
        : return : True <=> i and j belongs to the same component.
        : raise IllegalArgumentException : Raise an exception if either element is not in the union set
    '''
        
    if i == j:
      if 0 <= i < self.n:
        return True
      else:
        raise Exception("IllegalArgumentException")
    
    root_i = self.find_root(i)
    root_j = self.find_root(j)  
    
    return root_i == root_j

  def union(self, i, j):
    ''' Perform the union of two components, if they aren't unified yet.
        : param i : The first element.
        : param j : The second element, to be unified with i's component.
        : raise Exception: Raise an exception if either element is not in the 
                          union set (through find_root).
        : return : The size of the newly created component 
    '''

    root_i = self.find_root(i)
    root_j = self.find_root(j)    
    if root_i == root_j:
      return self.set_size[root_i]
    
    if self.set_size[root_i] <=  self.set_size[root_j]:
      self.set[root_i] = root_j
      self.set_size[root_j] += self.set_size[root_i]
      return self.set_size[root_i]
    else:
      self.set[root_j] = root_i
      self.set_size[root_i] += self.set_size[root_j]
      return self.set_size[root_j]

  def __str__(self):
    ''' : override :
    '''
    res = [str(range(self.n)), str(self.set), str(self.set_size)]
    return "\n".join(res)
    

          
if __name__ == '__main__':
  
  def test_UF():
    ''' Test the structure '''
    u = UnionFind(4)
    #print u
        
    assert not u.connected(2, 3)
    u.union(2,3)
    assert u.connected(2, 3)
    u.union(2,1)
    assert u.connected(2, 3)
    #print u
    u.add_element()
    assert not u.connected(2,4)
    u.union(0,4)
    assert u.connected(4,0)
    assert not u.connected(2,4)
    #print u  
  #end of test_UF definition
  test_UF()