import java.util.ArrayList;
import java.util.HashSet;


/**
 * 
 * @author mlarocca
 * 
 * A Patricia Trie (aka Radix Tree) is a prefix trie where common paths are compressed by storing the common substring in a single node.
 * This way each node has at list 2 children.
 *
 * @param <T>:	The type of Objects linked to the string prefixes: for example, if the strings are text to be matched, each prefix could be linked to a list of Strings
 * 				that contains it.
 */
public class PatriciaTrie<T>{

	/**
	 * 
	 * @author mlarocca
	 * 
	 * A single node of the tree.
	 * Each node contains 
	 * 		*	A label, i.e. the compressed path represented by the node (a substring of any prefix);
	 * 		*	A list of Children (empty for leaves);
	 * 		*	A list of T objects represented by (or connected) to the prefix.
	 */
	private class PatriciaTrieNode{
		private String label;
		private ArrayList<PatriciaTrieNode> children = new ArrayList<PatriciaTrieNode>();
		private HashSet<T> items = new HashSet<T>();
		
		/**
		 * Empty constructor.
		 * Label defaults to null, children and items list have already been initialized to empty containers.
		 *  
		 */
		public PatriciaTrieNode(){
			
		}
		
		/**
		 * Constructor
		 * @param l:	The label of the node;
		 * @param item:	An object of type T connected to the prefix represented by
		 * 				the path from the root of the tree to this node.
		 */
		public PatriciaTrieNode(String label, T item){
			this.label = label;
			this.items.add(item);
		}
		
		/**
		 * 
		 * @param label:	The label of the node;
		 * @param childrenListReference:	A reference to a list of nodes that
		 * 									must be set as children of the newly
		 * 									created node.
		 * 						WARNING:	The list passed MUST be already a copy
		 * 									of the original one, or MUST NOT be
		 * 									referenced elsewhere, 'cause it will
		 * 									not be cloned here.
		 * @param itemsList:	A list of T object associated with the prefix 
		 * 						represented by a path from the root to the current 
		 * 						node.
		 * 						WARNING: The list itself will be cloned, but the
		 * 								 contained object won't.
		 */
		@SuppressWarnings("unchecked")
		public PatriciaTrieNode(String label, ArrayList<PatriciaTrieNode> childrenListReference, HashSet<T> itemsList){
			this.label = label;
			this.children = childrenListReference;	//Note:	Children are kept in lessicographic order
			this.items = (HashSet<T>)(itemsList.clone());
		}

		
		/**
		 * Search a string in the tree starting at the current node.
		 * 
		 * @param s:	The query string;
		 * @return:		-	If the string is a substring of the label of any 
		 * 					children of this node, a reference to this node will
		 * 					be returned;
		 * 				-	If the any of the children's label is a substring of
		 * 					the search string, it will search the remaining of the
		 * 					string starting from that children, and return the
		 * 					result of the recursive call;
		 * 				-	Otherwise, there is no match for the search string.
		 */
		public PatriciaTrieNode search(String s){
			int l = 0, r = children.size()-1, pos = 0;
			char tmp_c, c;
			try{
				//If the search string is empty or null, return null
				//Needed to prevent crash when empty string or null are searched
				c = s.charAt(0);
			}catch(StringIndexOutOfBoundsException e){
				return null;
			}
			//Binary search on the first character of the string and of the children's label
			while (l <= r){
				pos = (l+r)/2;
				PatriciaTrieNode child = children.get(pos);
				String label = child.label;
				int l_len = label.length();
				tmp_c = label.charAt(0);
				if (tmp_c == c){
					int i = 1;
					int s_len = s.length();
					
					int n = Math.min(s_len, l_len);
					for (; i < n; i++){
						if (s.charAt(i) != label.charAt(i)){
							break;
						}
					}
					if (i == s_len){
						return child;
					}else if (i == l_len){
						return child.search(s.substring(i));
					}else{
						return null;
					}
				}else if (tmp_c < c){
					l = pos + 1;
				}else{
					r = pos - 1;
				}
			}

			return null;
		}

		
		/**
		 * Insert a new string (and all its prefixes) into the subtree rooted in
		 * this node.
		 * -	If the string is a prefix of any of this node's children's label,
		 * 		then it just adds the item associated with it to that node's 
		 * 		items list.
		 * -	If any of the children's label is a prefix of the new string, adds
		 * 		the item to that node's list and then recursively insert the rest
		 * 		of the string starting from that same node;
		 * -	If any of the children's label is a partial match to the string
		 * 		(meaning a prefix of the search string matches a prefix of the
		 * 		node's label) then splits that node at the first difference and
		 * 		continues the insertion of the rest of the string from the newly
		 * 		created node.
		 * -	Otherwise, creates a new node and adds it to this node's children.		
		 * 
		 * @param s:	The string to insert;
		 * @param item:	The T object associated with the string to insert;
		 * 
		 */
		public void insertChild(String s, T item){
			int size = children.size(), l = 0, r = size - 1, pos = 0;
			int s_len = s.length();
			char tmp_c, c;
			try{
				//If the search string is empty or null, return null
				//Needed to prevent crash when empty string or null are searched
				c = s.charAt(0);
			}catch(StringIndexOutOfBoundsException e){
				return ;
			}
			//Binary search on the first character of the new string
			while (l <= r){
				pos = (l+r)/2;
				PatriciaTrieNode child = children.get(pos);
				String label = child.label;
				
				tmp_c = label.charAt(0);
				if (tmp_c == c){
					//The first character of the new string matches the first
					//character of one of the children's label. 
					int l_len = label.length();
					int n = Math.min(l_len, s_len);
					int i = 1;
					
					for (; i < n; i++){
						if (label.charAt(i) != s.charAt(i)){
							break;
						}
					}
					
					if (i < l_len){
						//The new string partially matches node's label
						String restOfl = label.substring(i);
						child.label = s.substring(0, i);
						
						PatriciaTrieNode new_child = new PatriciaTrieNode(restOfl, child.children, child.items);
						child.children = new ArrayList<PatriciaTrieNode>(2);	//old var has exausted its life
						child.children.add(new_child);
						child.items.add(item);
						if (i < s_len){
							String restOfs = s.substring(i);
							new_child = new PatriciaTrieNode(restOfs, item);
							if ( restOfl.compareTo(restOfs) < 0){
								child.children.add(new_child);
							}else{
								child.children.add(0, new_child);
							}
						}
					}else if (i < s_len){
						//Node's label is a prefix of the new string
						child.items.add(item);
						String restOfs = s.substring(i);
						child.insertChild(restOfs, item);
					}else{
						//The new string is a prefix of node's label
						child.items.add(item);
					}
					return ;
				}else if (tmp_c < c){
					l = pos + 1;
				}else{
					r = pos - 1;
				}
			}

			//No path even partially matches the new string: a new node must be added to the tree.
			PatriciaTrieNode node = new PatriciaTrieNode(s, item);
			this.children.add(l, node);
			return ;
		}
		

		/**
		 * Removes a new string (and all its prefixes) from the subtree rooted in
		 * this node, if there's any match.
		 * 
		 * 
		 * @param s:	The string to insert;
		 * @param item:	The T object associated with the string to delete;
		 * 
		 */		
		public void removeItem(String s, T item){
			int l = 0, r = children.size()-1, pos = 0;
			char tmp_c, c;
			try{
				//If the search string is empty or null, return null
				//Needed to prevent crash when empty string or null are searched
				c = s.charAt(0);
			}catch(StringIndexOutOfBoundsException e){
				return ;
			}
			//Binary search on the string's first character;
			while (l <= r){
				pos = (l+r)/2;
				PatriciaTrieNode child = children.get(pos);
				String label = child.label;
				int l_len = label.length();
				tmp_c = label.charAt(0);
				if (tmp_c == c){
					//At least one prefix of the string matches this child
					child.items.remove(item);
					int i = 1;
					int s_len = s.length();
					
					int n = Math.min(s_len, l_len);
					for (; i < n; i++){
						if (s.charAt(i) != label.charAt(i)){
							break;
						}
					}
					
					if (i == l_len && i < s_len){
						//The node's label is a prefix of the string to remove
						child.removeItem(s.substring(i), item);
						return ;
					}else{
						//There can be no further match
						return ;
					}
				}else if (tmp_c < c){
					l = pos + 1;
				}else{
					r = pos - 1;
				}
			}

		}
	}
	 
	/**
	 * root:	Root of the RadixTree
	 */
	private PatriciaTrieNode root = new PatriciaTrieNode();
	
	/**
	 * Inserts a new string, and all its prefixes, into the tree.
	 * 
	 * @param label:	The string to add;
	 * @param item:		The item associated with the string.
	 */
	public void insertString(String label, T item){
		root.insertChild(label, item);
	}

	/**
	 * Removes a string and all its prefixes from the tree.
	 * It travels from the root of the tree along the path corresponding to the 
	 * string and removes the object associated with the string from the items
	 * list of each node visited.
	 * 
	 * @param s:	The string to remove;
	 * @param item:	The object associated with the string.
	 */
	public void removeString(String s, T item){
		root.removeItem(s, item);
	}
	
	/**
	 * Search a string in the tree and return the set of item stored in the
	 * node corresponding to the end of the string.
	 * 
	 * @param s:	The string to search;
	 * @return:		A Container (HashSet) filled with the objects associated with
	 * 				the entire string (possibly an empty container).
	 */
	public HashSet<T> search(String s){
		try {
			return root.search(s).items;
		}catch(NullPointerException e){
			return null;
		}
	}
	
	/**
	 * Search a list of string in the tree and return the set of item stored in
	 * the node corresponding to the end of the string.
	 * 
	 * @param sArray:	An array of strings to search;
	 * @return:		A Container (HashSet) filled with the objects associated with
	 * 				all of the strings in the query array (if no such object exists,
	 * 				it returns an empty list.	
	 */
	public HashSet<T> search(String[] sArray){
		HashSet<T> results, tmp_result, tmp;
		try{
			results = search(sArray[0]);
		}catch(IndexOutOfBoundsException e){
			return null;
		}
		
		int n = sArray.length;
		for (int i = 1; i < n; i++){
			try{
				if (results.isEmpty()){
					return results;
				}
				tmp_result = search(sArray[i]);
				tmp = new HashSet<T>(results.size());
				for (T item: tmp_result){
					if (results.contains(item)){
						tmp.add(item);
					}
				}
				results = tmp;				
			}catch(NullPointerException e){
				return null;
			}
		}
		return results;
	}


}	
