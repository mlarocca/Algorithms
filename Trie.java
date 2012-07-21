import java.io.IOException;
import java.util.ArrayList;


/**
 * 
 * @author mlarocca
 *
 * A Trie (Prefix Tree) where to each string inserted in the tree can be associated
 * one object of a generic type.
 * This implementation DOES NOT deal with duplicate keys: every time a string in
 * the tree is inserted, the previous value associated with the string is overwritten.
 * 
 * Leaves should correspond to strings in the trie (might not be so because of a lazy
 * implementation of the delete method).
 * Intermediate nodes can either correspond to string in the trie (if the item field
 * is not null) or to intermediate paths (if item == null).
 *
 * @param <T>	-	The type of objects this container can hold.
 */
public class Trie<T>{

	/**
	 * Trie's root.
	 */
	private TrieNode root = new TrieNode();

	private class TrieNode{
		
		private char edgeLabel;	//Represent the label of the edge from the parent of this node;
		private final ArrayList<TrieNode> children = new ArrayList<TrieNode>();	//children are stored in lexicographic order)
		private T item = null;
		
		/**
		 * Empty constructor (used to create trie's root).
		 * The associated item is init to null, and the list of children is initialized to an empty list.
		 */
		public TrieNode(){
			
		}
		
		/**
		 * Constructor.
		 * The associated item is init to null, and the list of children is initialized
		 * to an empty list.
		 * @param c:	The label of the edge that connects this node to its parent.
		 */
		public TrieNode(char c){
			this.edgeLabel = c;
		}
		
		
		/**
		 * Search if the current node has a child connected by an edge labeled
		 * with the given character - i.e., it searches if there is a path from
		 * these node towards the bottom of the tree which starts with the
		 * given character.
		 * 
		 * 
		 * @param c:	The character to search
		 * @return
		 */
		public TrieNode search(char c){
			int l = 0, r = children.size() - 1, pos = 0;
			char tmp_c;
			
			//Binary search on the edges to the children (they are stored in lexicographic order).
			while (l <= r){
				pos = (l + r) / 2;
				tmp_c = children.get(pos).edgeLabel;
				if (tmp_c == c){
					return children.get(pos);
				}else if (tmp_c < c){
					l = pos + 1;
				}else{
					r = pos - 1;
				}
			}

			return null;
		}

		/**
		 * Insert a new edge leaving this node, if an edge with the same label
		 * isn't already present.
		 * 
		 * @param c:	The label of the edge to insert.
		 * @return:	The child of this node that is connected to it by an edge
		 * 			whose label is the specified character (possibly a newly
		 * 			created edge).
		 */
		public TrieNode insertNode(char c){
			int size = children.size(), l = 0, r = size - 1, pos = 0;
			char tmp_c;
			//Binary search over the edges to the children (sorted lexicographically)
			while (l <= r){
				pos = (l + r) / 2;
				TrieNode child = children.get(pos);
				tmp_c = child.edgeLabel;
				if (tmp_c == c){
					//The edge already exist => returns it
					return child;
				}else if (tmp_c < c){
					l = pos + 1;
				}else{
					r = pos - 1;
				}
			}
			
			//The edge doesn't exist: a new node needs to be created
			TrieNode node = new TrieNode(c);
			this.children.add(l, node);
			return node;
		}
		
		/**
		 * Change the object associated with the string corresponding to the
		 * path from the root of the trie to this node;
		 * 
		 * @param item:	The new object to store
		 */
		public void setItem(T item){
			this.item = item;
		}
			
		/**
		 * Sets the object associated with the path from the root to this node
		 * to null - i.e., it removes the string corresponding to that path
		 * from the trie.
		 * 
		 * @return: True <=> the item has been correctly removed;
		 */
		public boolean removeItem(){
			if (this.item == null){
				return false;
			}
			this.item = null;
			return true;
		}
		
		
		/**
		 * Checks whether a node is still useful or can be deleted;
		 * 
		 * @return:		True <=> the node can be safely deleted from the tree
		 * 						 (iff it has no children and no string is 
		 * 						  associated with a path up to this node)
		 */
		public boolean isEmpty(){
			return this.item == null && this.children.size() == 0;
		}

	}
	
	/**
	 * Insert a string into the trie, together with an object associated with it.
	 * 
	 * @param s:	The string to insert;
	 * @param item:	The object associated with the string to insert.
	 */
	public void insertString(String s, T item){
		char[] cArray = s.toCharArray();
		TrieNode node = root;
		//Insert the string into the trie, char by char, by adding one edge for each one of its char.
		for (char c: cArray){
			node = node.insertNode(c);
		}
		node.setItem(item);
	}

	/**
	 * Removes a string previously inserted into the trie.
	 * 
	 * @param s:	The string to remove;
	 * 
	 * @return:	True <=> the string was stored in the trie and has been removed correctly.
	 */
	public boolean removeString(String s){
		char[] cArray = s.toCharArray();
		ArrayList<TrieNode> stack = new ArrayList<TrieNode>();
		TrieNode node = root;
		for (char c: cArray){
			try{
				node = node.search(c);
				stack.add(node);
			}catch(NullPointerException e){
				//If search returns null, the string isn't in the trie;
				return false;
			}
		}
		try{
			if (!node.removeItem()){
				//The string wasn't in the trie
				return false;
			}

			if (node.isEmpty()){
				char c, tmp_c;
				int l, r, pos, n = stack.size() - 1;
				ArrayList<TrieNode> children;
				stack.remove(n--);	//Removes the node corresponding to the string deleted from the stack;
				
				//Deletes nodes of the path from the root to the node corresponding to the deleted string
				//until a not empty node is found, or the root is reached
				//(removes nodes that has become obsolete)
				do{
					c = node.edgeLabel;
					node = stack.remove(n--);	//Next element on the stack is the parent of the TrieNode previously stored in node.
					children = node.children;
					
					//Binary search on the edges to the children to find the position of the child node.
					l = 0;
					r = children.size() - 1;
					while (l <= r){
						pos = (l + r) / 2;
						tmp_c = children.get(pos).edgeLabel;
						if (tmp_c == c){
							children.remove(pos);
							break;
						}else if (tmp_c < c){
							l = pos + 1;
						}else{
							r = pos - 1;
						}
					}				
				}while (n >= 0 && node.isEmpty());	//n >= 0 <=> !stack.isEmpty()
			}
			
		}catch(NullPointerException e){
			//If node is null, the string isn't in the trie;
			return false;
		}
		//The string has been correctly removed
		return true;
	}

	

	/**
	 * Removes a string previously inserted into the trie.
	 * 
	 * @param s:	The string to remove;
	 * 
	 * @return:	True <=> the string was stored in the trie and has been removed correctly.
	 */
	public boolean lazyRemoveString(String s){
		char[] cArray = s.toCharArray();
		TrieNode node = root;
		for (char c: cArray){
			try{
				node = node.search(c);
			}catch(NullPointerException e){
				//If search returns null, the string isn't in the trie;
				return false;
			}
		}
		try{
			node.removeItem();
		}catch(NullPointerException e){
			//If node is null, the string isn't in the trie;
			return false;
		}
		//The string has been correctly removed
		return true;
	}
	
	/**
	 * Searches a string to test if it belongs to the trie.
	 * 
	 * @param s:	The string to search;
	 * @return:	If the string is stored into the tree, the item associated
	 * 			with it is returned; otherwise returns null.
	 */
	public T search(String s){
		char[] cArray = s.toCharArray();
		TrieNode node = root, child;
		for (char c: cArray){
			try{
				child = node.search(c);
				node = child;
			}catch(NullPointerException e){
				return null;
			}
		}
		try{
			return node.item;			
		}catch(NullPointerException e){
			return null;
		}
	}
	
}
