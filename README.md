Algorithms
==========

General purpose implementation of advanced algorithms

1) 	PatriciaTrie (aka RadixTree)	-	Java
	Radix trees are a space-optimized trie data structures where each node with only one child is merged with its child. The result is that every internal node has at least two children. Unlike in regular tries, edges can be labeled with sequences of characters as well as single characters. This makes them much more efficient for small sets (especially if the strings are long) and for sets of strings that share long prefixes.
	(http://en.wikipedia.org/wiki/Radix_tree)
	In this implementation, when a string is inserted in the tree, an object is passed along with it; a reference to this object is stored in every node of the tree corresponding to a prefix of the string inserted.
	For example, if the strings inserted into the tree are titles of papers, these objects could be the full papers' text.
	If one is not interested in such features but only in establishing wheter or not a given prefix is stored into the tree, the list of associated objects may be replaced with a counter, for example.