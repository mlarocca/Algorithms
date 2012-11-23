'''Edmonds-Karp algorithm
    Computes the maximum flow from source to sink    
    @param edges: A dict whose keys are edge tuples, while the values are the capacity associated with each edge
                  Restrictions: if (u,v) is in edges, (v,u) can't be
                  Every value is OK as vertex label, but None    
    @return: the value of maximum flow, and the effective flow matrix
''' 
def edmonds_karp(edges, source, sink):
  
  adj = {}  #Adjacency matrix
  capacity = {} #Edges capacity
  flow = {} #Flow for graph's edges and residual edges
  
  for edge in edges:
    (u,v) = edge
    
    try:
      adj[u].append(v)
    except KeyError:
      adj[u] = [v]
    flow[edge] = 0
    capacity[edge] = edges[edge]
    
    
    #also consider the residual edge, with capacity and flow initially null
    edge = (v,u)
    try:
      adj[v].append(u)
    except KeyError:
      adj[v] = [u]  

    flow[edge] = 0
    capacity[edge] = 0
  
  n = len(adj)  
  queue = [None] * n 
  
  
  
  '''Find a path from source to sink, if any (using BFS)
  '''
  def find_path_BFS():
    head = 0
    queue[head] = source
    tail = 1
 
    parents = {source : None}
    M = {source: float('inf')}  #Not needed in this cause flow is either -1, 0 or 1
    
    while head < tail:
      u = queue[head]
      head += 1
      for v in adj[u]:
        if (not v in parents):
          edge = (u,v)
          residual = capacity[edge] - flow[edge]
          if residual > 0:            
            M[v] = min(M[u], residual)
            if v == sink:
              path_flow = M[v]
              flow[edge] += path_flow
              flow[(v,u)] -= path_flow                           
              v = parents[u]
              while v != None:
                flow[(v,u)] += path_flow
                flow[(u,v)] -= path_flow                   
                u = v
                v = parents[v]
              return path_flow
            else:
              parents[v] = u
              queue[tail] = v
              tail += 1
    #No path to sink node
    return 0
  
  partial_flow = find_path_BFS()
  while partial_flow != 0:
    partial_flow = find_path_BFS()

  return sum(flow[(source, dest)] for dest in adj[source]), flow



'''Relabel-to-Front algorithm
    Computes the maximum flow from source to sink
    @param edges: A dict whose keys are edge tuples, while the values are the capacity associated with each edge;
                  Restrictions: if (u,v) is in edges, (v,u) can't be
                  Every value is OK as vertex label, but None
    @return: the value of maximum flow, and the effective flow matrix
''' 
def relabel_to_front(edges, source, sink):
  adj = {}  #Adjacency matrix
  capacity = {} #Edges capacity
  flow = {} #Flow for graph's edges and residual edges
  
  for edge in edges:
    (u,v) = edge
    
    try:
      adj[u].append(v)
    except KeyError:
      adj[u] = [v]
    flow[edge] = 0
    capacity[edge] = edges[edge]
    
    
    #also consider the residual edge, with capacity and flow initially null
    edge = (v,u)
    try:
      adj[v].append(u)
    except KeyError:
      adj[v] = [u]  

    flow[edge] = 0
    capacity[edge] = 0
  
  n = len(adj)  

  height = {}           # height of node
  excess = {}           # flow into node minus flow from node
  current = {}          #next neighbour to be evaluated
  neighbours = {}       #next neighbour to be evaluated

  for u in adj:
    height[u] = excess[u] = current[u] = 0
    neighbours[u] = len(adj[u])   
  
  # node "queue"
  v_list = [u for u in adj if u != source and u != sink]
  
  def push(u, v):
    send = min(excess[u], capacity[(u,v)] - flow[(u,v)])
    flow[(u,v)] += send
    flow[(v,u)] -= send
    excess[u] -= send
    excess[v] += send
  
  def relabel(u):
    # find smallest new height making a push possible,
    # if such a push is possible at all
    try:
      height[u] = min([height[v] for v in adj[u] if capacity[(u,v)] > flow[(u,v)]])  + 1
    except:                         #except ValueError
      return #height[u] = n
  
  def discharge(u):
    while excess[u] > 0:
      try:
        # check next neighbour
        v = adj[u][current[u]]
      except IndexError:
        # we have checked all neighbours. must relabel
        relabel(u)
        current[u] = 0
        v = adj[u][0]
        
      if height[u] > height[v] and capacity[(u,v)] > flow[(u,v)]:
        push(u, v)
      else:
        current[u] += 1
  
  height[source] = n    # longest path from source to sink is less than n long
  excess[source] = float('inf')    # send as much flow as possible to neighbours of source
  for u in adj[source]:
    push(source, u)
  
  p = 0
  examined = 0
  k = len(v_list)
  while examined < k:       
    u = v_list[p]
    old_height = height[u]
    discharge(u)
    if height[u] > old_height:
    #v_list.insert(0, v_list.pop(p)) # move to front of v_list
    #p = 0 # start from front of v_list
      examined = 0
    else:
      p = (p + 1) % k
      examined += 1
    
  return sum(flow[(source, dest)] for dest in adj[source]), flow


if __name__ == "__main__":
  #Example
  example_graph = {("s",1): 16, ("s",2): 40, (1,2): 10, (1,3): 12, (3,2): 9, (2,4): 14, (4,3): 7, (3,"t"): 20, (4,"t"): 4}
  print edmonds_karp(example_graph, "s", "t")
  print relabel_to_front(example_graph, "s", "t")  