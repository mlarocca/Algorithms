from sets import Set
'''Node constructor
  @param l:  The label of the node;
  @param item:  An item connected to the prefix represented by
          the path from the root of the tree to this node.
'''     
def __create_leaf(label="", item=None):
  if item:
    return {"label": label, "items": Set([item]), "children":[]}
  else:
    return {"label": label, "items": Set(), "children":[]}


'''Node constructor
  @param l:  The label of the node;
  @param item:  An item connected to the prefix represented by
          the path from the root of the tree to this node.
'''     
def __create_inner_node(label, children, items):
  return {"label": label, "items": items, "children": children}




'''Applies binary search to look for the string s in the subtree rooted in node
'''
def __binary_search(node, s):
  
  l = pos = 0
  size = len(node["children"])

  if size > 0: 
    r = size - 1
    s_len = len(s)

    try : #try/except used instead of if as a speedup
      #If the search string is empty or null, return null
      #Needed to prevent crash when empty string or null are searched
      c = s[0]
    except:
      return None, None, None, None, l
        
    #Binary search on the first character of the string and of the children's label
    while l <= r:
      pos = (l+r)/2
      child = node["children"][pos]
      label = child["label"]
      l_len = len(label)
      
      tmp_c = label[0]

      
      if tmp_c == c: 
        s_len = len(s)
        
        n = min(s_len, l_len)
        i = 1
        while i < n:
          if s[i] != label[i]:
            break
          else:
            i += 1
      
        #Arriving here means the two strings are equals for the common parts 
        return child, i, s_len, l_len, l        
      elif tmp_c < c:
        l = pos + 1
      else:
        r = pos - 1
        
  return None, None, None, None, l

'''
Search a string in the tree starting at the current node.

@param s:  The query string;
@return:    -  If the string is a substring of the label of any 
          children of this node, a reference to this node will
          be returned;
        -  If the any of the children's label is a substring of
          the search string, it will search the remaining of the
          string starting from that children, and return the
          result of the recursive call;
        -  Otherwise, there is no match for the search string.
'''
def __node_search(node, s):

  child, i, s_len, l_len, l = __binary_search(node, s)

  if child == None:
    return None
  elif i == s_len:
    return child
  elif i == l_len:
    return __node_search(child, s[i:])
  else:
    return None    
    
'''
Insert a new string (and all its prefixes) into the subtree rooted in
this node.
-  If the string is a prefix of any of this node's children's label,
    then it just adds the item associated with it to that node's 
    items list.
-  If any of the children's label is a prefix of the new string, adds
    the item to that node's list and then recursively insert the rest
    of the string starting from that same node;
-  If any of the children's label is a partial match to the string
    (meaning a prefix of the search string matches a prefix of the
    node's label) then splits that node at the first difference and
    continues the insertion of the rest of the string from the newly
    created node.
-  Otherwise, creates a new node and adds it to this node's children.    

@param s:  The string to insert;
@param item:  The T object associated with the string to insert;
'''
def __node_insert(node, s, item):
#DEBUG  print "node ", s, item
  child, i, s_len, l_len, new_child_pos = __binary_search(node, s)

  if child == None:
    #No path even partially matches the new string: a new node must be added to the tree.      
    new_node = __create_leaf(s, item)
    node["children"].insert(new_child_pos, new_node)
  elif i < l_len:
#DEBUG    print   child["label"], s, i, s_len, l_len, l
    #The new string partially matches node's label
    rest_of_label = child["label"][i:]
    child["label"] = child["label"][:i]
    new_child = __create_inner_node(rest_of_label, child["children"], child["items"].copy())
    child["children"] = []
    child["children"].append(new_child)
    child["items"].add(item)
    if i < s_len:
      rest_of_s = s[i:]
      new_child = __create_leaf(rest_of_s, item)
      
      if rest_of_label < rest_of_s :
        child["children"].append(new_child)
      else:
        child["children"].insert(0, new_child)
  elif i < s_len:
    #Node's label is a prefix of the new string
    child["items"].add(item)
    rest_of_s = s[i:]
    __node_insert(child, rest_of_s, item)
  else:
    #The new string is a prefix of node's label
    child["items"].add(item)


'''
Removes a new string (and all its prefixes) from the subtree rooted in
this node, if there's any match.

WARNING: The path is NOT removed from the tree, only the item associated 
         with it is
 
@param node: Current node
@param s:  The string to remove;
@param item:  The T object associated with the string to delete

@return: True  <=> the deletion was completely successfull
         False <=> item isn't found among the stored items, or s isn't found in the tree path
'''   
def __node_remove_item(node, s, item):
  
  child, i, s_len, l_len, l = __binary_search(node, s)
  success = True
  
  if child != None:
    #At one prefix of the string matches this child
    try:
      child["items"].remove(item)
    except KeyError:
      success = False
   
    if i == l_len and i < s_len:
      #The node's label is a prefix of the string to remove
      return success and __node_remove_item(child, s[i:], item);
    else:
      #There can be no further match
      return success
  else:  
    return False


'''
Removes a string and all its prefixes from the tree.
It travels from the root of the tree along the path corresponding to the 
string and removes the object associated with the string from the items
list of each node visited.

WARNING: The path is NOT removed from the tree, only the item associated 
         with it is

@param s:  The string to remove;
@param item:  The object associated with the string.

@return: True  <=> the deletion was completely successfull
         False <=> item isn't found among the stored items, or s isn't found in the tree path
'''
def trie_remove_item(root, label, item):
  return __node_remove_item(root, label, item)
  #DEBUG  print root

'''
Inserts a new string, and all its prefixes, into the trie.
@param root:    The root of the trie
@param label:  The string to add;
@param item:    The item associated with the string.
'''
def trie_insert(root, label, item):
  __node_insert(root, label, item)
  #DEBUG  print root
  
'''
Search a string in the tree and return the set of item stored in the
node corresponding to the end of the string.
@param root:    The root of the trie
@param s:  The string to search;
@return:    A set filled with the objects associated with
             the entire string (possibly an empty set).
'''
def trie_search(root, s):
  try:
    return __node_search(root, s)["items"]
  except TypeError:
    #If the search return None, then it has no items field.
    #Try/except is used to speed up happy cases
    return Set()
    

'''Creates the root of the tree (an empty node)
  '''
def create_trie():
  return __create_leaf()    
    
if __name__ == "__main__":
  #Unit Testing
  def test():
    trie = create_trie()
    trie_insert(trie, "test", "test str")
    #print trie_search(trie, "test")
    trie_insert(trie, "alfa", "alfa str")

    
    assert( "test str" in trie_search(trie, "test")  )    
    assert( "alfa str" in trie_search(trie, "alfa")  )
    assert( len(trie_search(trie, "testo")) == 0  )
    trie_insert(trie, "tempo", "tempo str")
    print trie_search(trie, "test")
    assert( "test str" in trie_search(trie, "test")  )
    assert( "alfa str" in trie_search(trie, "alfa")  )
    assert( "tempo str" in trie_search(trie, "tem")  )
    assert( "tempo str" in trie_search(trie, "tempo")  )
    search = trie_search(trie, "te")
    assert( "tempo str" in search and "test str" in search and not "alfa str" in search  )    
    search = trie_search(trie, "t")
    assert( "tempo str" in search and "test str" in search and not "alfa str" in search  )   
    #print trie_search(trie, "test")
    trie_insert(trie, "test", "test str2")
    print trie_search(trie, "test") 
    assert( "test str2" in trie_search(trie, "test")  )
    print trie     
    print trie_search(trie, "tet")
    assert( len(trie_search(trie, "tet")) == 0 )
    
    def trie_properties_test(node, father_label):
      label = father_label + node["label"]
      l_len = len(label)
      print node["items"]
      for item in node["items"]:
        try:
          assert(item[:l_len] == label)
        except:
          print "ERROR ", label, item
          print node
      for child in node['children']:
        trie_properties_test(child, label)
     
    trie_properties_test(trie, "")



    print  trie_remove_item(trie, "test", "teststr")

    assert("test str" in trie_search(trie, "test")  )
    print  trie_remove_item(trie, "test", "test str")
    print trie
    assert(not "test str" in trie_search(trie, "test")  )
    trie_insert(trie, "test", "test str")
    
    assert( "test str" in trie_search(trie, "test")  )    
    
    
    trie_properties_test(trie, "")

    print  trie_remove_item(trie, "test", "test str")
    print trie
    assert(not "test str" in trie_search(trie, "test")  )
    trie_properties_test(trie, "")
     
  test()