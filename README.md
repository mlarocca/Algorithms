Algorithms
==========

General purpose implementation of advanced algorithms

1) 	PatriciaTrie (aka RadixTree)	-	Java
	Radix trees are a space-optimized trie data structures where each node with only one child is merged with its child. The result is that every internal node has at least two children. Unlike in regular tries, edges can be labeled with sequences of characters as well as single characters. This makes them much more efficient for small sets (especially if the strings are long) and for sets of strings that share long prefixes.
	(http://en.wikipedia.org/wiki/Radix_tree)
	In this implementation, when a string is inserted in the tree, an object is passed along with it; a reference to this object is stored in every node of the tree corresponding to a prefix of the string inserted.
	For example, if the strings inserted into the tree are titles of papers, these objects could be the full papers' text.
	If one is not interested in such features but only in establishing wheter or not a given prefix is stored into the tree, the list of associated objects may be replaced with a counter, for example.
	
	
2)	Trie (aka Prefix Tree)	-	Java 
	A trie, or prefix tree, is an ordered tree data structure that is used to store a dynamic set or associative array where the keys are usually strings. Unlike a binary search tree, no node in the tree stores the key associated with that node; instead, its position in the tree defines the key with which it is associated. All the descendants of a node have a common prefix of the string associated with that node, and the root is associated with the empty string. Values are normally not associated with every node, only with leaves and some inner nodes that correspond to keys of interest.
	In this implementation, to each string inserted in the Trie must be associated a single object, stored together with the string, and the presence or absence of this object marks a path in the trie as one of the stored strings or an intermediate path.
	Insertion of multiple instances of the same string is not supported: the latter occurrence of a string inserted will overwrite the object previously associated with the same string.
	
	To support multiple occurrences of the same string, a list of objects might be stored.
	If no object needs to be associated with a string and the it is simply needed to assess whether or not a string has been inserted in the trie, 2 solutions are possible:
	1)	A Trie<Boolean> can be created, without modifying anything, at the cost of passing a fake not-null value as the second parameter of the insert function;
	2)	The implementation can be slightly changed, removing the generics code and adding a boolean parameter to the Node class.
	
	The remove method is implemented in a "lazy" way: it won't actually remove any node from the trie, it will just set to null the object associated with the string to remove.
	This approach prevent from searching the trie for prefixes of its strings, so in the future a non-lazy removal will be added (it can be done by adding parent pointers to each node or, to avoid this extra space and synchronization overhead, during the deletion nodes in the path can be added to a stack).
	The lazy approach, however, speeds up significantly the deletion at the cost of keeping a bigger tree (since dead edges and paths won't be removed for the tree), so it is particularly useful only when it is expected to have a much greater number of insertion than deletion from the tree. 