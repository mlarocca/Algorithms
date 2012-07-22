'''
@author: mlarocca
'''

from time import time
from random import random, randrange, seed
from math import copysign
from copy import deepcopy

from numpy import mean, std


''' Genetic Algorithm
    The class is designed on the Template Pattern: it implements just the sketch
    of a genetic algorithm, with a random initialization, and then a cycle, with
    a new __population created at each iteration from the __population at the previous
    one.
    This class specifies only the selection algorithm (round robin selection)
    and the elitism criteria; the details of chromosomes' structure, of the 
    crossover and of the mutations algorithms (including the number of different
    kinds of mutations), together with their ratio of application, are completely
    left to the specific class that models evolving individuals.
    
    Of course the Template pattern isn't fully applied in this case because the
    further generalization needed would make the implementation unnecessarily
    complicated and would also penalize the performance.
'''
class genetic_algorithm():
    

    
    ''' Constructor
        Sets up the parameters
        @param individual_initializer:     A reference to the constructor function
                                           of the individuals used.
        @param population_size:     The number of individuals to be included in the
                                    __population to evolve;
                                    WARNING: this value MUST be greater than or
                                             equal to 4 otherwise crossover would
                                             be meaningless (and selection would
                                             raise an exception anyway);
        @param time_limit:    The maximum time that can be spent on optimizing;
                                WARNING:    the actual time spent will be slightly
                                            larger than this limit, because only
                                            when the limit is already crossed the
                                            main function will return;
    '''
    def __init__(self, individual_initializer, population_size, time_limit):
        assert(population_size >= 4)
        assert(time_limit > 0)
        
        self.__individual_initializer = individual_initializer
        self.__population_size = population_size
        self.__time_limit = time_limit        
      
    ''' Genetic Algorithm main
        Although it has been created specifically for this challenge, it sketches
        a general purpose genetic algorithm, needing just a few adjustments
        to be used for different problems.
        The application of the Template Design Pattern is limited in order to
        achieve clarity, readability and good performance.
        
        The algorithm goes through the following steps:
        1)    Generates randomly an initial population; The details of the
                generation of the single individual are left to the
                problem-specific class that models individual;
        2)    Repeats the following cycle, until the allotted time is over:
                2.a)    Let's the best element(s) of the previous generation
                        pass through to the next one unchanged (elitism);
                2.b)    Until the new population hasn't been fully generated:
                        2.b.1)    Randomly selects couple of elements from the old
                                    generation and let them reproduce (either by
                                    crossover or cloning);
                        2.b.2)    Applies mutation(s) to the couple of elements produced
                                    by the reproduction routine at the previous step;
                        2.b.3)    Adds each of the new elements to the new population,
                                    in the right position (the population is kept
                                    in reverse order with respect to the fitness -
                                    higher fitness means better elements);
                INVARIANT: after the iteration is completed, the first
                            element in the population, if it models a valid solution,
                            is also the best solution found so far.
        3)    Returns The solution modeled by the first element of the population
        
        @param file_log:    Optional parameter: the file to which write log info, like
                            intermediate results.
        @return:    (best_score, best_element)
                    A couple whose first element is the score of the best solution found,
                    and the second one is the solution itself.
    '''  
    def start(self, file_log = None): 
        #Need to ensure randomization
        seed(time())

        
        self.__population = self.__init_population(self.__individual_initializer,
                                                   self.__population_size)
        
        #DEBUG
        if file_log != None:
            it = 0
        
        start_time = time()     #Doen't count the initialization time, in order to have the main
                                #cycle executed at least once!
                    
        while time() - start_time < self.__time_limit:
            #Elitism: the best element always passes to the next generation
            new_population = [self.__population[0]]
            #If __population_size is even, then, since new elements are added in pairs,
            #to match the size extends elitism to the second best individual
            if not self.__population_size % 2:
                new_population.append(self.__population[1])
            M = len(new_population)
            while M < self.__population_size:
                #Select 2 individuals from the previous __population, and then have them reproduced to
                #the next one, either by crossover or cloning (see __reproduction function)
                (new_individual_1, 
                 new_individual_2) = self.__reproduction(
                                                self.__selection(self.__population, 
                                                             len(self.__population)))

                for individual in [new_individual_1, new_individual_2]:
                    #Applies the mutations according to the rates specified by the Individual's class itself
                    for mutation in individual.MUTATIONS:
                        self.__apply_mutation(mutation)
                    
                    #Tries to insert the new element in the existing __population
                    for i in range(M):
                        #Higher __fitness individuals have better rank
                        if self.__fitness(individual) > self.__fitness(new_population[i]):
                            new_population.insert(i, individual)
                            break
                    if i==M-1:
                        #Element must be added to the end of the list
                        new_population.append(individual)
                    M+=1
                
            self.__population = new_population  
            
            #DEBUG
            if file_log != None:
                it += 1
                fitnesses = map(lambda ind: self.__fitness(ind), new_population)
                file_log.writelines('\tIteration # {} - Fitness: Best={}, mean={}, std={}\n'
                                    .format(it, self.__fitness(new_population[0]), 
                                           mean(fitnesses), std(fitnesses)))
        
        best_fitness = self.__fitness(self.__population[0])
        
        return best_fitness, self.__population[0]
      

    ''' Creates a population of the specified size of Individual individuals,
        using the "constructor" method for the Individuals specified when the
        Genetic Algorithm was itself init.
        
        @param individual_initializer:     A reference to the constructor function
                                           of the individuals used.
        @param population_size:    The desired size for the population set;
        @return:    The new population created.
    '''    
    def __init_population(self, individual_initializer, population_size):
        new_population = []
        for i in xrange(population_size):
            new_population.append(individual_initializer())
        return new_population  
    
    ''' Shortcut to compute any individual's fitness
        @param individual:    The member of the __population whose fitness must be computed;
        @return:    The value of the individual's fitness.
    '''
    def __fitness(self, individual):
        return individual.computeFitness()
    
    ''' Shortcut to perform "reproduction" on a couple of individuals;
        The crossover reproduction is applied with probability CROSSOVER_PROBABILITY,
        otherwise the individuals just clone themselves into the new generation;
        
        @param individual_1: The first element that is going to reproduct;
        @param individual_2: The second element that is going to reproduct;
    '''    
    def __reproduction(self, (individual_1, individual_2)):
        if random() < individual_1.CROSSOVER_PROBABILITY:
            #Applies crossover (100*CROSSOVER_PROBABILITY)% of the times...
            (new_individual_1, new_individual_2) = individual_1.crossover(individual_2)
        else:
            #... otherwise the individuals are just copied to next generation
            (new_individual_1, new_individual_2) = (individual_1.copy(), individual_2.copy())

        return (new_individual_1, new_individual_2)
      
    ''' Shortcut to perform one of the kinds of mutations designed for the
        specific problem;
        
        @param mutation:    the function that actually perform the mutation;
        @param mutation_probability:    the probability that the mutation is actually
                                  applied.
    '''  
    def __apply_mutation(self, (mutation, mutation_probability)):
        if random() < mutation_probability:
            mutation()

    
    ''' Round robin selection;
        The how_many elements are chosen randomly from the __population;
        For each element returned, two candidates are taken randomly from a uniform
        distribution over the __population set, then with probability SELECT_BEST_PROBABILITY
        the best of the two is chosen, and with prob. 1.-SELECT_BEST_PROBABILITY the least
        fit one is chosen.
        The probability SELECT_BEST_PROBABILITY is left to the specific problem to choose;
        If SELECT_BEST_PROBABILITY == 0.5 each element is selected exactly with uniform
        probability, otherwise the mean is shifted towards one of the sides in
        proportion to the difference SELECT_BEST_PROBABILITY - 0.5, in the same way as
        the mean of the minimum between two uniform random numbers in [0,1] 
        becomes 1/3 and the mean of the maximum becomes 2/3;
        
        @param __population:    The __population from which to choose the individuals;
        @param size:    The size of the __population from which to choose;
                        NOTE:   size can be lower than len(__population), allowing
                                to use only a subset of the __population;
        @param how_many:    The number of elements to be selected;
        @return:    The list of elements chosen.
    '''
    def __selection(self, population, size, how_many = 2):
        #INVARIANT:    len(__population) >= size >= how_many * 2
        indices = [i for i in range(size)]
        chosen = []
        for i in range(how_many):
            #Chooses two individuals randomly
            first = indices[randrange(size)]
            indices.remove(first)   #Doesn't allow repetitions (Every index generated here must be different)
            size -= 1
            second = indices[randrange(size)]    
            indices.remove(second)   #Doesn't allow repetitions
            size -= 1
                       
            if random() < population[first].SELECT_BEST_PROBABILITY:
                #The one with better rank is chosen
                mul = 1
            else:
                #The one with worst rank is chosen
                mul = -1
            
            if mul * population[first].computeFitness() > mul * population[second].computeFitness():
                chosen.append(self.__population[first])
            else:
                chosen.append(self.__population[second])
 
        return chosen


#END of class genetic_algorithm

   
   
''' Class Individual
    A Individual Object models the solution to the problem in such a way that
    it can be used as the basis of the genetic algorithm sketched in the class
    genetic_algorithm.
    This is a base class from which real individuals should be modeled,
    according to the specific problem.
    
    Chromosomes are represented array of flags.
'''     
class Individual():
    
    ''' Constant:   alias for a value denoting a valid solution (each 
    '''
    __VALID_SOLUTION = 1.
    ''' Constant:   alias for a value denoting an invalid subsed (one that
                    violate some constraint).'''
    __NOT_VALID_SOLUTION = 0.
    
    ''' The probability that during round robin selection it is chosen the best
        individual from the dueling couple .'''
    SELECT_BEST_PROBABILITY = .7
    ''' The probabilty that crossover is applied during individuals reproduction.'''
    CROSSOVER_PROBABILITY = .8;

    
    ''' Constructor: define a constant set containing reference to the mutation
        methods coupled with the probability with which they should be applied;
        The chromosome of the individual can either be passed as a parameter, 
        or generated at random.
    ''' 
    def __init__(self, chromosome_size, chromosome=None):
        assert(chromosome_size > 0)
        ''' Only one kind of mutation is applied, and it is stored together with
            its ratio of application for this problem.
            Subclasses may add mutation methods as well.'''
        self.MUTATIONS = [(self.__mutation_1, 0.5)]
        
        if chromosome != None:
            self.__chromosome = deepcopy(chromosome)
        else:
            self.__chromosome = self.__random_init(chromosome_size)
            
        self.__changed = True
        
        

    ''' Initialize the element mask, which denotes the subset of the Universe
        of the Stories characterizing a single element.
        The probability distribution over the space of the subsets is uniform.
        @param N:    The size of the Universe
        @return:    A list of 0 and 1, representing a bit mask that denotes
                    a subset of the Universe (i.e. the set of all the Stories
                    in the DB).
    '''
    def __random_init(self, N):
        
        '''
            @return:    0 or 1 with probability 1 over 2.
        '''
        def random_bit():
            if random() < 0.5:
                return 1
            else:
                return 0
              
        return [random_bit() for i in xrange(N)]


    ''' Shortcut for a deepcopy of the element.
        @return:    a deepcopy of the individual.
    '''
    def copy(self):
        copy_instance = deepcopy(self)
        return copy_instance


   
    ''' Computes the fitness associated with this Individual
        WARNING:    This method MUST be overridden by a problem specific version.
        
        The base class version returns just the number of ones in the chromosome.
        To speed up runtime, the fitness is computed again only when the individual
        has been changed since the last time it was computed.
        
        @return:    The indidual's fitness, as the tuple described above.           
    '''           
    def computeFitness(self):
        if self.__changed:
            self._fitness = 0
            for i in xrange(len(self.__chromosome)):
                if self.__chromosome[i]:
                    self._fitness += 1
            self.__changed = False

        return self._fitness

    ''' Crossover    
        Single point Crossover is used for individuals reproduction: it is randomily
        chosen one point in the middle of the chromosome, and the 4 halves created
        by dividing the two individuals' genomes are mixed together to form
        2 new individuals.
        
        @param other:    The other subset that will be used for reproduction;
        @return:    A couple of brand new individuals.
    '''
    def crossover(self, other):
        N = len(self.__chromosome)
        if N<3:
            return self.copy(), other.copy()
        
        point = 1 + randrange(N-2)                  #Crossing point must be non-trivial
        new_mask_1 = self.__chromosome[:point] + other.__chromosome[point:]
        new_mask_2 = other.__chromosome[:point] + self.__chromosome[point:]
        return Individual(N, new_mask_1), Individual(N, new_mask_2)
    
    ''' Mutation1
        One flag, chosen at random, is flipped, so that one gene previously
        activated won't be anymore, or viceversa;
        
        WARNING: Mutation1 changes the modify the object it's called on!
    '''
    def __mutation_1(self):
        point = randrange(len(self.__chromosome))
        self.__chromosome[point] = int( copysign(self.__chromosome[point]-1, 1) )
        self.__changed = True    
        
#END of class Individual


''' Simple example: ones counter
'''
if __name__ == '__main__':
    from sys import stdout
    chromosome_size = 50
    initializer = lambda: Individual(chromosome_size)
    ga = genetic_algorithm(initializer, 20, 0.25)   #20 individuals, 0.25 seconds time limit.
    fitness, solution = ga.start(stdout)    #Print log info on stdout