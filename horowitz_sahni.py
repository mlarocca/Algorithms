'''
@author: mlarocca
'''

''' Performs, iteratively, the Horowitz-Sahni algorithms for 0-1 KP problem.
    INVARIANT: the elements to put in the knapsack must be ordered according
                to the ratio value/cost (vector e), from the highest to the lowest.
    Tries to add as much elements to the set as possible according to their
    scaled value ("forward move") and then, when it funds a critical element 
    (i.e. one that cannot be added to the knapsack) estimates an upper bound
    (in particular Dantzig's upper bound) for the maximum value that is possible
    to get with the current elements included in the solution:
    if this bound is lower than the best value obtained so far, prunes the
    recursion and perform a backtracking move, looking for the closest '1'
    in the subset bit mask (if it exists), and removing the corresponding
    element from the knapsack.
    To improve performance, some features of the Martello-Toth algorithm are 
    added (for instance a tighter bound than Danzing's is computed).
    
    @param p:   List of elements' values;
    @param w:   List of elements' weights;
    @param e:   List of elements' scaled values: e[i] = p[i]/w[i]
                The elements available are sorted according to the 'e' vector.
                The i-th element has value p[i], weight w[i].
    @param N:   The number of elements available;
    @param c:   Total capacity of the knapsack;
    @return:    A tuple with 3 elements:
                1)    The best value found for the knapsack (the solution
                      of the problem);
                2)    The total weight of the solution;
                3)    A bitmask identifying the elements belonging to the
                      solution.
'''
def horowitz_sahni(p, w, e, N, c):
    
    if N == 0:
        return 0, 0, []
        
    mask = [0] * N
    best_solution_mask = mask[:]
    
    value = best_solution_value = 0
    weight = best_solution_weight = 0
    size = best_solution_size = 0
    
    j = 0
    while True:
        while j < N:
            
            #Try a forward move        
            pos = j
            
            initial_value = value
            initial_heigh = weight
            initial_size = size
            
            while pos < N:
                
                #First tries a forward move, if possible
                if w[pos] > c - weight:
                    break
                else:
                    size += 1
                    mask[pos] = 1
                    value += p[pos]
                    weight += w[pos]
                    pos += 1

            if pos >= N:
                #Completed one "depth first search" visit in the solution 
                #space tree: now must break off the while cycle
                break

            upper_bound = value + (int)(e[pos] * (c - weight))
            
            if upper_bound < best_solution_value:
                #The forward move would not led us to a better solution,
                #so it performs backtracking

                #Brings the situation back at before the forward move
                for k in xrange(j,N):
                    mask[k] = 0
                
                value = initial_value 
                weight = initial_heigh
                size = initial_size

                #Looks for a possible backtracking move
                pos = j - 1
                while True:
                    try:
                        while mask[pos] == 0:
                            pos -= 1
                    except IndexError:
                        #pos < 0: No more backtracking possible
                        return best_solution_value, best_solution_weight, best_solution_mask
                    else:
                        #Exclude the element from the knapsack
                        mask[pos] = 0
                        size -= 1
                        
                        value -= p[pos]
                        weight -= w[pos]
                        j = pos + 1

                        #Computes the upper bound on the score (According to the elements
                        #that can be added to the knapsack)
                        bound_height = weight
                        value_bound = 0
                        for i in xrange(j, N):
                            if w[i] > c - bound_height:
                                break
                            
                            value_bound += p[i]
                            bound_height += w[i]
                        
                        try:
                            value_bound += (int)(e[i] * (c - bound_height))
                        except IndexError:
                            pass
                            
                        upper_bound = value + value_bound
                        
                        if upper_bound > best_solution_value:
                            break               
            else:
                #The forward move was successful: discards the next element
                #(which couldn't have been added because violates the
                #knapsack capacity) and tries to perform more f. moves.
                j = pos + 1
                
        #INVARIANT: j == N:
        #Completed one "depth first search" visit in the solution space tree.
        if value > best_solution_value:
            #Checks current solution
            best_solution_mask = mask[:]
            best_solution_size = size
            best_solution_weight = weight
            best_solution_value = value
            
            if best_solution_size == N: #best_solution_value == U or 
                return best_solution_value, best_solution_weight, best_solution_mask
        
        try:   
            if mask[N-1] == 1:
                mask[N-1] = 0
                size -= 1               
                value -= p[N-1]
                weight -= w[N-1]
        except IndexError:
            pass
        
        #Tries a backtracking move
        pos = N - 2
        while True:
            try:
                while mask[pos] == 0:
                    pos -= 1
            except IndexError:
                #pos < 0: No more backtracking possible
                return best_solution_value, best_solution_weight, best_solution_mask
            else:
                #Exclude the element from the knapsack
                mask[pos] = 0
                size -= 1
                value -= p[pos]
                weight -= w[pos]
                j = pos + 1
                
                #Computes the upper bound on the score (According to the elements
                #that can be added to the knapsack)
                bound_height = weight
                value_bound = 0
                for i in xrange(j, N):
                    if w[i] > c - bound_height:
                        break
                    
                    value_bound += p[i]
                    bound_height += w[i]
                
                try: #if i < N:
                    value_bound += (int)(e[i] * (c - bound_height))
                except IndexError:
                    pass
                    
                upper_bound = value + value_bound
                
                if upper_bound > best_solution_value:
                    break
