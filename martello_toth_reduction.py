'''
    @author: mlarocca

    Tries to reduce the 0-1 Knapsack problem by finding the elements that must
    be part of any optimal solution (set J1) and those that can't appear in an
    optimal solution (set J0). The core is represented by all the elements that
    neither belongs to J1 or J0, and the exact solution may now be computed on
    this smaller set rather than on the whole set of elements: the global
    solution will then be the union of the solution on the core problem and
    the elements in the set J1.
    
    The critical element (whose index is s) is the only one that might appear 
    in both sets: if it is so and the intersection between the two sets is not
    empty, then the reduction is not valid.
    
    During the reduction process, a value p_star is computed: this is a lower
    bound to the optimal solution. If the sum of the core problem solution and
    the value of the elements in J1 is lower than p_star, then p_star is the
    solution to the problem (it might be worth keeping track of the elements
    corresponding to the highest value of p_star found, for this reason).

    @param p:   List of elements' values;
    @param w:   List of elements' weights;
    @param e:   List of elements' scaled values: e[i] = p[i]/w[i]
                The elements available are sorted according to the 'e' vector.
                The i-th element has value p[i], weight w[i].
    @param N:   The number of elements available;
    @param c:   Total capacity of the knapsack;
    @return:    The sets of indices J1 and J0, as described above. 
'''

def martello_toth_reduction(p, w, e, N, c):
    p_bar = [0]
    w_bar = [0]
    
    
    def binary_search(vec, size, value):
        l = 0
        r = size
        while l <= r:
            s = (l+r)/2
            if s == 0:
                if value <= vec[0]:
                    break
                else:
                    l = 1
            elif s == size:
                if vec[s-1] <= value:
                    break
                else:
                    r = s - 1
            else:
                if vec[s-1] <= value and value < vec[s]:
                    break
                elif value < vec[s-1]:
                    r = s - 1
                else:   #w_bar[s] <= c
                    l = s + 1
        return s
        
    value = 0
    weight = 0
    #INVARIANT:    Stories must be considered in descending _scaled_value order
    for i in xrange(N):
        value += p[i]
        weight += w[i]
        p_bar.append(value)
        w_bar.append(weight)

#DEBUG    print p_bar
#DEBUG    print w_bar
    

    u_zero = [0]
    u_one = []
    
    
    s = binary_search(w_bar, N+1, c)
    
    p_star = p_bar[s-1]     #value of the set J1
    c_bar = c - w_bar[s-1]
    
#DEBUG    print s, p_star, c_bar
    
    for j in range(s, N):   #Lists start from index '0', so indices are shifted by 1
        if w[j] <= c_bar: 
            p_star += p[j]
            c_bar -= w[j]
        j += 1
#DEBUG    print p_star, c_bar
    
    for j in range(s):
        c_bar = c + w[j]
        s_bar = binary_search(w_bar, N+1, c_bar)
        
        c_bar -= w_bar[s_bar-1]
        
        if s_bar < N:
            scaled_value_plus_one = e[s_bar]    #Indices are shifted by 1
        else:
            scaled_value_plus_one = 2e63-2
            
        if s_bar > 1:
            scaled_value_minus_one = e[s_bar - 2]    #Indices are shifted by 1
        else:
            scaled_value_minus_one = 2e63-2
            
        u_zero.append(p_bar[s_bar-1] - p[j] + 
              max((int)(c_bar*scaled_value_plus_one),
                  (int)(p[s_bar-1]
                        - float(w[s_bar-1] - c_bar) * scaled_value_minus_one)
                   )
              )
        p_star = max(p_star, 
                     p_bar[s_bar-1] - p[j])

#DEBUG        print j, s_bar, c_bar, u_zero[j+1], p_star
    for j in range(s-1, N): #Indices are shifted by 1
        
        c_bar = c - w[j]        #Indices are shifted by 1
        s_bar = binary_search(w_bar, N+1, c_bar)

        c_bar -= w_bar[s_bar-1]

        if s_bar < N:
            scaled_value_plus_one = e[s_bar]    #Indices are shifted by 1
        else:
            scaled_value_plus_one = 2e63-2
            
        if s_bar > 1:
            scaled_value_minus_one = e[s_bar-2]     #Indices are shifted by 1
        else:
            scaled_value_minus_one = 2e63-2
               
        u_one.append(p_bar[s_bar-1] + p[j] + 
              max((int)(c_bar * scaled_value_plus_one),
                  (int)(p[s_bar-1]
                        - (w[s_bar-1] - c_bar) * scaled_value_minus_one)
                   )
              )
        p_star = max(p_star, 
                     p_bar[s_bar-1] + p[j])

#DEBUG        print j, s_bar, c_bar, u_one[j-s+1], p_star

    J1 = [j-1 for j in range(1, s + 1) if u_zero[j] <= p_star]
    J0 = [j-1 for j in range(s, N + 1) if u_one[j-s] <= p_star]       
    
    return J1, J0