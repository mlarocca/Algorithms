from math import sqrt
from array import array
class ss_tree(object):
    
    ''' Creates the empty root of an SS-tree.
        @param max_elements_per_cluster:    The max number of children for each intermediate node,
                                            and the max number of points for each leaf.
    '''
    def __init__(self, max_elements_per_cluster=2):
        self.__root = {'points': [], 'leaf':True, 'parent': None, 'x':0., 'y':0.}
        assert(max_elements_per_cluster > 1)
        
        self.__max_elements_per_cluster = max_elements_per_cluster        
        self.__split_size = self.__max_elements_per_cluster / 2
    
    ''' Inserts a point (topic) in a SS-tree; If necessary, splits the tree node in which the point was inserted
        and fixes the tree structure from that node up to the root.
        
        @param new_point:   The point to be inserted;
                            The point must be a dictionary with at least 3 fields:
                            -    'x':    Point's x coordinate;
                            -    'y':    Point's y coordinate;
                            -    'data':    The data associated with the point.
    '''
    def insert(self, new_point):
        x_new_point = new_point['x']
        y_new_point = new_point['y']
        
        #Looks for the right leaf (the one with the closest centroid) to which the new_point should be added.
        #INVARIANT:    The empty tree's root is a (empty) leaf.
        node = self.__root
        while not node['leaf']:
            children = node['children']
            child = children[0]
            min_dist = (child['x'] - x_new_point) ** 2 + (child['y'] - y_new_point) ** 2
            min_index = 0
            for i in range(1,len(children)):
                child = children[i]
                dist = (child['x'] - x_new_point) ** 2 + (child['y'] - y_new_point) ** 2
                if dist < min_dist:
                    min_index = i
                    min_dist = dist
            node = children[min_index]
            

        #Now adds the new point to the leaf it has found.
        
        #INVARIANT: node is a leaf
        points = node['points']
        if len(points) < self.__max_elements_per_cluster:
            #No split neeeded to add the point to this node
            
            #Can add the new_point to this node
            old_x_node = x_node = node['x']
            old_y_node = y_node = node['y']     
            
            #Compute the new centroid for the node
            n_p = len(points)
            x_node *= n_p
            y_node *= n_p
            x_node += x_new_point
            y_node += y_new_point
            points.append(new_point)
            n_p += 1
            x_node /= n_p
            y_node /= n_p
            node['x'] = x_node
            node['y'] = y_node
                
            #Compute node's radius and variance      
            radius = 0.
            x_var = y_var = 0.
            for point in points:
                #INVARIANT: points don't have radius
                x_dist = (x_node - point['x']) ** 2
                y_dist = (y_node - point['y']) ** 2
                radius = max(radius, x_dist + y_dist)
                #We don't need the exact variance, we can do fine with an estimate based on max distance form the centroid
                x_var = max(x_var, x_dist)
                y_var = max(y_var, y_dist)
            node['radius'] = sqrt(radius)
            node['x_var'] = x_var
            node['y_var'] = y_var
            
            #Propagates the change all the way to the root
            node_parent = node['parent']
            while node_parent != None:
                tmp_x = x_node_parent = node_parent['x']
                tmp_y = y_node_parent = node_parent['y'] 
                n_p = len(node_parent['children'])
                x_node_parent *= n_p
                y_node_parent *= n_p
                x_node_parent += x_node - old_x_node
                y_node_parent += y_node - old_y_node
                old_x_node = tmp_x
                old_y_node = tmp_y
                x_node_parent /= n_p
                y_node_parent /= n_p   
                node_parent['x'] = x_node_parent
                node_parent['y'] = y_node_parent 
                                           
                radius = 0.
                x_var = y_var = 0.
                for child_node in node_parent['children']:
                    x_dist = (x_node_parent - child_node['x']) ** 2
                    y_dist = (y_node_parent - child_node['y']) ** 2
                    radius = max(radius, sqrt(x_dist + y_dist) + child_node['radius'])                  
                    #We don't need the exact variance, we can do fine with an estimate based on max distance form the centroid
                    x_var = max(x_var, x_dist + child_node['radius'] ** 2)
                    y_var = max(y_var, y_dist + child_node['radius'] ** 2)
               
                node_parent['radius'] = radius
                node_parent['x_var'] = x_var
                node_parent['y_var'] = y_var
                                                
                node = node_parent
                node_parent = node['parent']
        else:
            #len(children) == max_elements_per_cluster => The leaf must be split
            
            #Splits along the direction with highest variance
            if node['x_var'] >= node['y_var']:
                points.sort(key=lambda p: p['x'])
            else:
                points.sort(key=lambda p: p['y'])
            
            #The new nodes have exactly half the elements of the old one
            new_node_1 = {'points': points[:self.__split_size], 'leaf': True}
            new_node_2 = {'points': points[self.__split_size:], 'leaf': True}          
        
            
            #Compute the centroids for the new nodes
            for new_node in [new_node_1, new_node_2]:
                points = new_node['points']
                x_node = 0.
                y_node = 0.
                for point in points: 
                    x_node += point['x']
                    y_node += point['y']
                n_p = len(points)
                x_node /= n_p
                y_node /= n_p
                
                new_node['x'] = x_node
                new_node['y'] = y_node
    
            #Adds the new point to the one of the two new nodes that is closest to the old centroid
            x_node = node['x']
            y_node = node['y']
            dist_1 = (x_node - new_node_1['x']) ** 2 + (y_node - new_node_1['y']) ** 2 
            dist_2 = (x_node - new_node_2['x']) ** 2 + (y_node - new_node_2['y']) ** 2
            
            if (dist_1 > dist_2):
                new_node = new_node_2
                new_node_2 = new_node_1
                new_node_1 = new_node
            
            #INVARIANT: at this point new_node_1 is the one of the two new nodes closest to the old node's centroid
            #Adds the new point to new_node_1
            points = new_node_1['points']       
            n_p = len(points)  
            #Updates new_node_1's centroid
            x_node = new_node_1['x']
            y_node = new_node_1['y']
            x_node *= n_p
            y_node *= n_p            
            x_node += new_point['x']
            y_node += new_point['y']
            points.append(new_point)
            n_p += 1
            new_node_1['x'] = x_node / n_p
            new_node_1['y'] = y_node / n_p
                        
            #Compute the radius of the new nodes
            for new_node in [new_node_1, new_node_2]:
                
                x_node = new_node['x']
                y_node = new_node['y']
                
                radius = 0.
                x_var = y_var = 0.
                for point in new_node['points']:
                    #INVARIANT: point don't have radius
                    x_dist = (x_node - point['x']) ** 2
                    y_dist = (y_node - point['y']) ** 2
                    radius = max(radius, x_dist + y_dist)
                    #We don't need the exact variance, we can do fine with an estimate based on max distance form the centroid
                    x_var = max(x_var, x_dist)
                    y_var = max(y_var, y_dist)
                    
                new_node['radius'] = sqrt(radius)
                new_node['x_var'] = x_var
                new_node['y_var'] = y_var      
                                
            
            #INVARIANT: at this new_point new_node_1 is the closest to the centroid of node, so it takes its place among the
            #childrens of its parent
            node_parent = node['parent']
            
            if node_parent == None:
                #The node that has just been split was the root: so it must create a new root...
                self.__root = {'children': [new_node_1, new_node_2], 'leaf':False, 'parent': None, 
                        'x': (new_node_1['x'] + new_node_2['x'])/2,
                        'y': (new_node_1['y'] + new_node_2['y'])/2}
                x_dist_1 = (new_node_1['x'] - self.__root['x']) ** 2
                x_dist_2 = (new_node_2['x'] - self.__root['x']) ** 2
                y_dist_1 = (new_node_1['y'] - self.__root['y']) ** 2
                y_dist_2 = (new_node_2['y'] - self.__root['y']) ** 2                                
                self.__root['radius'] = max(sqrt(x_dist_1 + y_dist_1) + new_node_1['radius'],
                                     sqrt(x_dist_2 + y_dist_2) + new_node_2['radius'])
                self.__root['x_var'] = max(x_dist_1 + new_node_1['radius'] ** 2, 
                                    x_dist_2 + new_node_2['radius'] ** 2)
                self.__root['y_var'] = max(y_dist_1 + new_node_1['radius'] ** 2,
                                    y_dist_2 + new_node_2['radius'] ** 2)
                
                new_node_1['parent'] = new_node_2['parent'] = self.__root
                
                #... and return
                return                  
            else:
                #Replaces the old node (the one just split) with the closest of the newly created
                new_node_1['parent'] = node_parent
          
                node_parent['children'].remove(node)
                node_parent['children'].append(new_node_1)
            
    
                while node_parent != None:
                    node = node_parent
                    children = node['children']
                    
                    #Checks if there is still a node resulting from the split of one of its children
                    #INVARIANT:    new_node_2 is the farthest of the two resulting node from the split
                    if new_node_2:
                        
                        if len(children) < self.__max_elements_per_cluster:
                            #No need for farther splits: just append the new node
                            children.append(new_node_2)
                            new_node_2['parent'] = node
                            new_node_2 = None                   
                        else:
                            #Must split this node too
                            old_node = new_node_2
                            
                            #Split the children along the axes with the biggest variance
                            if node['x_var'] >= node['y_var']:
                                children.sort(key=lambda p: p['x'])
                            else:
                                children.sort(key=lambda p: p['y'])                            
                                
                            new_children = children[:self.__split_size]
                            new_node_1 = {'children': new_children, 'leaf': node['leaf']}
                            for child in new_children:
                                child['parent'] = new_node_1

                            new_children = children[self.__split_size:]
                            new_node_2 = {'children': new_children, 'leaf': node['leaf']}
                            for child in new_children:
                                child['parent'] = new_node_2                         
                           
                            #Compute the centroids
                            for new_node in [new_node_1, new_node_2]:
                                x_node = 0.
                                y_node = 0.
                                for child in new_node['children']: 
                                    x_node += child['x']
                                    y_node += child['y']
                                n_p = len(new_node['children'])
                                new_node['x'] = x_node / n_p
                                new_node['y'] = y_node / n_p

                            #Finds the one of the new nodes closest to the original centroid  
                            dist_1 = (node['x'] - new_node_1['x']) ** 2 + (node['y'] - new_node_1['y']) ** 2 
                            dist_2 = (node['x'] - new_node_2['x']) ** 2 + (node['y'] - new_node_2['y']) ** 2
                            
                            if (dist_1 > dist_2):
                                new_node = new_node_2
                                new_node_2 = new_node_1
                                new_node_1 = new_node   
                                
                            #INVARIANT:    At this point new_node_1 is the one of two nodes resulting from the split
                            #                closest to the orginal centroid
                            n_p = len(new_node_1['children'])
                            new_node_1['children'].append(old_node)
                            old_node['parent'] = new_node_1
                            
                            x_node = new_node_1['x']
                            y_node = new_node_1['y']
                            x_node *= n_p
                            y_node *= n_p
                            x_node += old_node['x']
                            y_node += old_node['y']
                            n_p += 1
                            new_node_1['x'] = x_node / n_p
                            new_node_1['y'] = y_node / n_p
                            
                            #Compute the radiuses and the variances
                            for new_node in [new_node_1, new_node_2]:

                                x_node = new_node['x']
                                y_node = new_node['y']
                                
                                radius = 0.
                                x_var = y_var = 0.
                                
                                for child_node in new_node['children']:
                                    x_dist = (x_node - child_node['x']) ** 2
                                    y_dist = (y_node - child_node['y']) ** 2
                                    radius = max(radius, sqrt(x_dist  + y_dist) + child_node['radius'])  
                                    #We don't need the exact variance, we can do fine with an estimate based on max distance form the centroid
                                    x_var = max(x_var, x_dist + child_node['radius'] ** 2)
                                    y_var = max(y_var, y_dist + child_node['radius'] ** 2)
                                
                                new_node['radius'] = radius
                                new_node['x_var'] = x_var
                                new_node['y_var'] = y_var  
                            
                            #Checks whether the root has been split                            
                            node_parent = node['parent']
                            if node_parent == None:
                                #Has just split the root
                                self.__root = {'children': [new_node_1, new_node_2], 'leaf':False, 'parent': None, 
                                        'x': (new_node_1['x'] + new_node_2['x'])/2,
                                        'y': (new_node_1['y'] + new_node_2['y'])/2}
                                x_dist_1 = (new_node_1['x'] - self.__root['x']) ** 2
                                x_dist_2 = (new_node_2['x'] - self.__root['x']) ** 2
                                y_dist_1 = (new_node_1['y'] - self.__root['y']) ** 2
                                y_dist_2 = (new_node_2['y'] - self.__root['y']) ** 2                                
                                self.__root['radius'] = max(sqrt(x_dist_1 + y_dist_1) + new_node_1['radius'],
                                                     sqrt(x_dist_2 + y_dist_2) + new_node_2['radius'])
                                self.__root['x_var'] = max(x_dist_1 + new_node_1['radius'] ** 2, x_dist_2 + new_node_2['radius'] ** 2)
                                self.__root['y_var'] = max(y_dist_1 + new_node_1['radius'] ** 2, y_dist_2 + new_node_2['radius'] ** 2)
                                new_node_1['parent'] = new_node_2['parent'] = self.__root
                                return                                  
                            else:
                                new_node_1['parent'] = node_parent   
                          
                                node_parent['children'].remove(node)
                                node_parent['children'].append(new_node_1)
                                
                                #node doesn't exist anymore, and for new_node_1 and new_node_2 everything has been computed
                                #and therefore can go to the next iteration
                                continue
                            
                    #Updates node's centroid, radius and variances                       
                    x_node = 0.
                    y_node = 0.
                    
                    for child_node in children:
                        x_node += child_node['x']
                        y_node += child_node['y']
                    
                    n_p = len(children)
                    x_node /= n_p
                    y_node /= n_p
                    node['x'] = x_node
                    node['y'] = y_node
                                         
                    radius = 0.
                    x_var = y_var = 0.
                    for child_node in children:
                        x_dist = (x_node - child_node['x']) ** 2
                        y_dist = (y_node - child_node['y']) ** 2
                        radius = max(radius, sqrt(x_dist + y_dist) + child_node['radius'])
                        x_var = max(x_var, x_dist + child_node['radius'] ** 2)
                        y_var = max(y_var, y_dist + child_node['radius'] ** 2)
                        
                    node['radius'] = radius
                    node['x_var'] = x_var
                    node['y_var'] = y_var                        
    
                    node_parent = node['parent']
        
        return      

        
    ''' Finds the k nearest points to the query point taking advantage of the
        SS Tree structure;
        A heap whose size is bounded to k is used to store the k closest
        distances to the query point (if at least k are found).
        To speed up performance, the heap is implemented as a static array 
        of doubles to store just the distances of the points, while 
        another dynamic list will hold couples (distance, point data) so
        that, once the traversal of the tree is ended, the k closest points
        can be filtered from this list using the distance of the k-th nearest
        neighbour (stored in heap[0]).
        
        @param (x0,y0):    Coordinates of the query point;
        @param k:    How many neighbours must be retrieved.
        @return:    The list of the data field of the k nearest neighbours,
                    sorted by proximity to the query point.
    '''     
    def k_nearest_neighbours(self, (x0, y0), k):
            assert(k > 0)
            heap = array('d', [0] * (k+1))       #INVARIANT:    no more than k results are needed
            #Init the heap to an empty max-heap
            heap_size = 0
            #Keeps track of the candidates to nearest neighbours found
            heap_elements = []          
            
            
            #Starts a search in the topics SS-tree;
            #All the topics are pushed in a bounded max-heap which holds at most k distances
            #(the k smallest ones) so that, once the heap is full, its first element is
            #the kth distance discovered so far, and this value can be used to prune the search
            #on the SS-tree.
            
            if self.__root['leaf']:
                #The tree has only one node, the root: so every point must be examined
                points = self.__root['points']
                for p in points:
                    data = p['data']
                    x = p['x']
                    y = p['y']

                    new_dist = sqrt((x - x0) ** 2 + (y - y0) ** 2)

                    if heap_size == k:
                        if new_dist > heap[0]:
                            #The heap is full: if the new value is greather than the kth distance,
                            #then it can't be one of the k nearest neighbour's distances                               
                            continue
                    
                        heap_elements.append((new_dist, data))                
                        pos = 0
                        # Bubble up the greater child until hitting a leaf.
                        child_pos = 2 * pos + 1    # leftmost child position
                        while child_pos < heap_size:
                            # Set childpos to index of greater child.
                            right_pos = child_pos + 1
                            if right_pos < heap_size and heap[child_pos] < heap[right_pos]:
                                child_pos = right_pos
                            # Move the greater child up.
                            if heap[child_pos] <= new_dist:
                                break
                            heap[pos] = heap[child_pos]
                            pos = child_pos
                            child_pos = 2*pos + 1
                        heap[pos] = new_dist           
                    else:
                        heap_elements.append((new_dist, data))                
                        heap[heap_size] = new_dist
                        pos = heap_size
                        heap_size += 1
                        # Follow the path to the root, moving parents down until finding a place
                        # newitem fits.
                        while pos > 0:
                            parent_pos = (pos - 1) >> 1
                            parent = heap[parent_pos]
                            if new_dist > parent:
                                heap[pos] = parent
                                pos = parent_pos
                            else:
                                break
                        heap[pos] = new_dist                    
            else:
                queue = []
                #Adds all the root's children to the queue, and examines them in order of increasing distance
                #of their border from the query point
                children = self.__root['children']
                for child in children:
                    dist = sqrt((child['x'] - x0) ** 2 + (child['y'] - y0) ** 2)
                    radius = child['radius']
                    if dist <= radius:
                        dist = 0
                    else:
                        dist -= radius
                    queue.append((dist, radius, child))

                queue.sort(key=lambda q:q[0], reverse=True)
                
                while len(queue) > 0:
                    (d, r, node) = queue.pop()
                    
                    if node['leaf']:
                        points = node['points']
                        for p in points:
                            data = p['data']
                            x = p['x']
                            y = p['y']

                            new_dist = sqrt((x - x0) ** 2 + (y - y0) ** 2)
                        
                            if heap_size == k:    
                                #The heap is full: if the new value is greather than the kth distance,
                                #then it can't be one of the k nearest neighbour's distances                       
                                if new_dist > heap[0]:                                   
                                    continue
                                
                                heap_elements.append((new_dist, data))
                                #heap[0] = new_dist
                                pos = 0
                                # Bubble up the greater child until hitting a leaf.
                                child_pos = 2 * pos + 1    # leftmost child position
                                while child_pos < heap_size:
                                    # Set childpos to index of greater child.
                                    right_pos = child_pos + 1
                                    if right_pos < heap_size and heap[child_pos] < heap[right_pos]:
                                        child_pos = right_pos
                                    # Move the greater child up.
                                    if heap[child_pos] <= new_dist:
                                        break
                                    heap[pos] = heap[child_pos]
                                    pos = child_pos
                                    child_pos = 2*pos + 1
                                heap[pos] = new_dist           
                            else:
                                heap_elements.append((new_dist, data))
                                heap[heap_size] = new_dist
                                pos = heap_size
                                heap_size += 1
                                # Follow the path to the root, moving parents down until it finds a place
                                #where new_item fits.
                                while pos > 0:
                                    parent_pos = (pos - 1) >> 1
                                    parent = heap[parent_pos]
                                    if new_dist > parent:
                                        heap[pos] = parent
                                        pos = parent_pos
                                    else:
                                        break
                                heap[pos] = new_dist
                                
                        #Checks if now the queue is full
                        if heap_size == k:
                            #If it is so, filters the queue
                            #The heap is full: if the distance of the border of the node from the query point
                            #is greather than the kth distance then no point in that node can be one of the
                            #k nearest neighbour's                              
                            d_max = heap[0]                                  
                            queue = [(d, r, n) for (d, r, n) in queue if d <= d_max]                                
                    else:
                        if heap_size < k:
                            for child in node['children']:
                                dist = sqrt((child['x'] - x0) ** 2 + (child['y'] - y0) ** 2)
                                radius = child['radius']
                                if dist <= radius:
                                    dist = 0
                                else:
                                    dist -= radius
                                queue.append((dist, radius, child))
                             
                            queue.sort(key=lambda q:q[0], reverse=True)
                        else:
                            d_max = heap[0]        
                            queue = [(d, r, n) for (d, r, n) in queue if d <= d_max]                            
                            for child in node['children']:
                                dist = sqrt((child['x'] - x0) ** 2 + (child['y'] - y0) ** 2)
                                radius = child['radius']
                                if dist <= radius:
                                    dist = 0
                                else:
                                    dist -= radius
                                
                                if dist <= d_max:
                                    #The heap is full: if the distance of the border of the node from the query point
                                    #is greather than the kth distance then no point in that node can be one of the
                                    #k nearest neighbour's                                       
                                    queue.append((dist, radius, child))

                            queue = sorted([(d, r, n) for (d, r, n) in queue if d <= d_max],
                                           key=lambda q:q[0], reverse=True)
            
            #Filters the possible nearest neighbours such that their distance is not greater than the the distance of the kth
            #nearest neighbour
            return [data for (d, data) in 
                        sorted([(d, data) for (d, data) in heap_elements if d <= heap[0]])]