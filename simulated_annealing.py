from copy import deepcopy
from random import randrange


''' Defines the base class that models a generic solution found by Simulated Annealing
    to a generic problem.
    Solution objects MUST have:
    *    A 'score' method (returning either a float or an int, must express how well
         a solution solves the problem;
    *    One or more 'mutation' methods: methods that enhance the solution in a problem specific way
    *    A 'mutation' field: a list of all the mutation methods supported
    
    Real solution classes can inherit from this stub class.
'''
class Solution(object):
    
    def __init__(self):
        #Stub: implement the real constructor here
        self.mutations = [self.mutation_1]
    
    ''' WARNING:
        The returned value MUST be strictly positive
    '''
    def score(self):
        #Stub: problem specific method, define it here or override
        return 0.
    
    @staticmethod
    def mutation_1(solution):
        #Stub: real mutation methods should return a (mutated) copy of the object
        return deepcopy(solution)


'''Example class'''
class OnesSolution(Solution):    
    def __init__(self, length):
        assert(length > 0)
        self.length = length
        self.string = [False] * length
        super(OnesSolution, self).__init__()
        pass
    
    ''' WARNING:
        The returned value MUST be strictly positive
    '''
    def score(self):
        score = 1 + len([el for el in self.string if el])
        assert(score > 0)
        return score
        
    @staticmethod
    def mutation_1(solution):
        temp_solution = deepcopy(solution)
        i = randrange(solution.length)
        solution.string[i] = not solution.string[i]
        return temp_solution


'''Simulated annealing main: until all the allotted time has been used, keeps restarting
   the annealing procedure and saves its result
   @param max_time: the maximum (indicative) execution time for the annealing, in seconds;
   @return: (best_score, best_solution)
           The best solution found by simulated annealing, and its score.
'''
def simulated_annealing(max_time):
    from random import random
    from math import e
    from time import time
    ''' Start temperature'''
    INITIAL_TEMPERATURE = 1.
    
    ''' How many times do we cool'''
    COOLING_STEPS = 100        #500
    
    ''' How much to cool each time'''
    COOLING_FRACTION = 0.97    
    
    ''' Number of mutations cycles for each temperature cooling step - lower makes it faster, higher makes it potentially better. '''
    STEPS_PER_TEMP = 50         #1000
    
    ''''Problem specific Boltzman's constant'''
    K = 0.1      

    
    ''' Stub for a method that builds a solution to the problem,
        randomly
    '''
    def initial_solution():
        #Stub
        return OnesSolution(20)   #Defer initialization to the Solution class
    


    ''' Single iteration of simulated annealing
        @return: (best_value, best_solution)
                best_solution is the the best solution to the problem that this cycle of simulated annealing could find, and best_value 
                is its score according to the problem's own metric.
                
    '''
    def annealing():
        temperature = INITIAL_TEMPERATURE
    
        solution = initial_solution()
        best_solution = deepcopy(solution)
        best_value = current_value = solution.score()
        
        for i in xrange(COOLING_STEPS):
            temperature *= COOLING_FRACTION
            start_value = current_value
            
            for j in xrange(STEPS_PER_TEMP):
                for mutation in solution.mutations:    
                    new_solution = mutation(solution)
                        
                    new_value = new_solution.score()
                    delta = new_value - current_value
    
                    if delta==0:    #No change to solution's score
                        continue
                                            
                    flip = random()
                    exponent = float(new_value) / delta * K / temperature
                    merit = e ** exponent
    
                    if delta > 0 : # ACCEPT-WIN
                        solution = deepcopy(new_solution)
                        current_value = new_value
                        if current_value > best_value:
                            best_value = current_value
                            best_solution = deepcopy(solution)
                            
                    elif merit > flip :  #ACCEPT-LOSS
                        solution = deepcopy(new_solution)
                        current_value = new_value

            if  (current_value-start_value) > 0.0 : # rerun at this same temperature
                temperature /= COOLING_FRACTION
    
        return (best_value, best_solution)

    start_time = time()
    best_solution = None
    best_score = 0

    #Continues until the execution exceeded the allotted time
    while time() < start_time + max_time:
        (score, solution) = annealing()
        if score > best_score:
            best_solution = deepcopy(solution)
            best_score = score

    return (best_score, best_solution)

if __name__ == '__main__':
    print simulated_annealing(0.5)