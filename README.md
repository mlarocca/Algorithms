Algorithms
==========

General purpose implementation of advanced algorithms

1)	Trie (aka Prefix Tree)	-	Java 
	A trie, or prefix tree, is an ordered tree data structure that is used to store a dynamic set or associative array where the keys are usually strings. Unlike a binary search tree, no node in the tree stores the key associated with that node; instead, its position in the tree defines the key with which it is associated. All the descendants of a node have a common prefix of the string associated with that node, and the root is associated with the empty string. Values are normally not associated with every node, only with leaves and some inner nodes that correspond to keys of interest.
	In this implementation, to each string inserted in the Trie must be associated a single object, stored together with the string, and the presence or absence of this object marks a path in the trie as one of the stored strings or an intermediate path.
	Insertion of multiple instances of the same string is not supported: the latter occurrence of a string inserted will overwrite the object previously associated with the same string.	
	
		To support multiple occurrences of the same string, a list of objects might be stored.
	If no object needs to be associated with a string and the it is simply needed to assess whether or not a string has been inserted in the trie, 2 solutions are possible:
	1)	A Trie<Boolean> can be created, without modifying anything, at the cost of passing a fake not-null value as the second parameter of the insert function;
	2)	The implementation can be slightly changed, removing the generics code and adding a boolean parameter to the Node class.	
	
		Two versions of the remove method are implemented:
	1) 	A "lazy" way: it won't actually remove any node from the trie, it will just set to null the object associated with the string to remove.
		This approach prevent from searching the trie for prefixes of its strings; the lazy approach, however, speeds up significantly the deletion at the cost of keeping a bigger tree (since dead edges and paths won't be removed for the tree), so it is particularly useful only when it is expected to have a much greater number of insertion than deletion from the tree.
	2) 	A thorough approach, which deletes dead paths when strings are removed from the trie. This is the suggested approach when string removal is expected to be a common operation on the trie (for dynamic tries).
	
		NOTE:	The two methods SHOULD NOT be mixed (once lazy, always lazy...). It is care of the caller to avoid such things, so you'd better leave only the method you want to be used when you add this code to your project.
	
2) 	PatriciaTrie (aka RadixTree)	-	Java
	Radix trees are a space-optimized trie data structures where each node with only one child is merged with its child. The result is that every internal node has at least two children. Unlike in regular tries, edges can be labeled with sequences of characters as well as single characters. This makes them much more efficient for small sets (especially if the strings are long) and for sets of strings that share long prefixes.
	(http://en.wikipedia.org/wiki/Radix_tree)
	In this implementation, when a string is inserted in the tree, an object is passed along with it; a reference to this object is stored in every node of the tree corresponding to a prefix of the string inserted.
	For example, if the strings inserted into the tree are titles of papers, these objects could be the full papers' text.
	If one is not interested in such features but only in establishing wheter or not a given prefix is stored into the tree, the list of associated objects may be replaced with a counter, for example.
	
3)	Horowitz-Sahni algorithm	-	Python
	H.S. algorithm is a branch and bound algorithm that efficiently solves the 0-1 Knapsack problem, provided that the elements to be inserted into the knapsack are sorted accordind to the ratio p[i]/w[i], from the largest to the smallest, where p[i] is the value of the i-th element and w[i] is its weight.
	An iterative version of the algorithm is provided; in the main cycle, it ries to add as much elements to the knapsack as possible according to their scaled value ("forward move") and then, when it funds a critical element (i.e. one that cannot be added to the knapsack) estimates an upper bound in particular Dantzig's upper bound) for the maximum value that is possible to get with the current elements included in the solution: if this bound is lower than the best value obtained so far, prunes the recursion and perform a backtracking move, looking for the closest '1' in the subset bit mask (if it exists), and removing the corresponding element from the knapsack. 
    To improve performance, some features of the Martello-Toth algorithm are 
    added (for instance a tighter bound than Danzing's is computed).

4) 	Martello-Toth reduction for 0-1 Knapsack 	-	Python
	Tries to reduce the 0-1 Knapsack problem by finding the elements that must be part of any optimal solution (set J1) and those that can't appear in an optimal solution (set J0). The core is represented by all the elements that neither belongs to J1 or J0, and the exact solution may now be computed on this smaller set rather than on the whole set of elements: the global solution will then be the union of the solution on the core problem and the elements in the set J1.    
    The critical element (whose index is s) is the only one that might appear in both sets: if it is so and the intersection between the two sets is not empty, then the reduction is not valid.    
    During the reduction process, a value p_star is computed: this is a lower to the optimal solution. If the sum of the core problem solution and the value of the elements in J1 is lower than p_star, then p_star is the solution to the problem (it might be worth keeping track of the elements corresponding to the highest value of p_star found, for this reason).

5)	Genetic Algorithm	-	Python
    The class is designed on the Template Pattern: it implements just the sketch of a genetic algorithm, with a random initialization, and then a cycle, with a new __population created at each iteration from the __population at the previous one.
    This class specifies only the selection algorithm (round robin selection) and the elitism criteria; the details of chromosomes' structure, of the  crossover and of the mutations algorithms (including the number of different kinds of mutations), together with their ratio of application, are completely left to the specific class that models evolving individuals.
	A base class for individuals, on which problem specific individuals might be modeled (also through inheritance) and a short example of how to use it are also provided.

6)	Simulated Annealing	-	Python
	The class is designed on the Template Pattern: it implements just the sketch of the simulated annealing algorithm, leaving the problem specific operation for the Solution class to specify.
	A base class for individuals, on which problem specific individuals might be modeled (also through inheritance) and a short example of how to use it are also provided.

7)	Queue, PriorityQueue	-	Javascript	(container.js)
	
8)	Graphs:	Depth-First Search, Breadth-First Search, Dijkstra, Prim	-	JavaScript	(graph.js, requires container.js)