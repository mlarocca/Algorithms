function node(k, v){
	that = {
			key:k,
			val:v,
			
			compareTo: 	function(othernode){
							return compareDistances(v, othernode.val);
						}
			}
	Object.preventExtensions(that);
	return that;
}

function vertex( label ){
	"use strict";
	
	var that = {}, col;
	
	Object.defineProperty( that, "getLabel", {
	   value: function(){
				return label;
				},
	   writable: false,
	   enumerable: false,
	   configurable: false
	});
	Object.defineProperty( that, "setLabel", {
	   value: function(newLabel){
				label = newLabel;
				},
	   writable: false,
	   enumerable: false,
	   configurable: false
	});
	
	Object.defineProperty( that, "equals", {
	   value: 	function(otherLabel){
					return label === otherLabel;
				},
	   writable: false,
	   enumerable: false,
	   configurable: false
	});

	Object.defineProperty( that, "color", {
	   get: function(){return col;},
	   set: function(c){
							if (!c){
								throw "Invalid color parameter";
							}
							c = c.toLowerCase();
							if ( c === "white" || c === "gray" || c === "black" ){
								col = c;
							}else{
								throw "Invalid color parameter";
							}
						},
	   enumerable: false,
	   configurable: false
	});
	
	Object.defineProperty( that, "isVertex", {
	   value: true,
	   writable: false,
	   enumerable: false,
	   configurable: false
	});
	
	Object.preventExtensions(that);
	
	return that;
}

function edge(src, dest, weight){
	"use strict";

	var that = {}, tipo;

	if (!src || !src.isVertex || !dest || !dest.isVertex){
		throw 	{
					name: "IllegalArgumentException",
					message: "Source and destination must be valid vertex"
				};
	}
	
	
	Object.defineProperty( that, "getSrc", {
	   value: function(){
				return src;
				},
	   writable: false,
	   enumerable: false,
	   configurable: false
	});
	
	Object.defineProperty( that, "getDest", {
	   value: function(){
				return dest;
				},
	   writable: false,
	   enumerable: false,
	   configurable: false
	});
	
	Object.defineProperty( that, "getWeight", {
	   value: function(){
				return weight;
				},
	   writable: false,
	   enumerable: false,
	   configurable: false
	});
	
	Object.defineProperty( that, "setWeight", {
	   value: function(w){
				weight = w;
				},
	   writable: false,
	   enumerable: false,
	   configurable: false
	});
	
	Object.defineProperty( that, "type", {
	   get: function(){return tipo;},
	   set: function(t){
							if (!t){
								throw "Invalid edge type parameter";
							}
							t = t.toLowerCase();
							if ( t === "tree" || t === "forward" || t === "back" || t === "cross" ){
								tipo = t;
							}else{
								throw "Invalid edge type parameter";
							}
						},
	   enumerable: false,
	   configurable: false
	});
	
	Object.defineProperty( that, "isTreeEdge", {
	   value: function(){	return (tipo === "edge");},
	   writable: false,
	   enumerable: false,
	   configurable: false
	});	
	
	Object.defineProperty( that, "isForwardEdge", {
	   value: function(){	return (tipo === "forward");},
	   writable: false,
	   enumerable: false,
	   configurable: false
	});	
	
	
	Object.defineProperty( that, "isBackEdge", {
	   value: function(){	return (tipo === "back");},
	   writable: false,
	   enumerable: false,
	   configurable: false
	});	
		
	Object.defineProperty( that, "isCrossEdge", {
	   value: function(){	return (tipo === "cross");},
	   writable: false,
	   enumerable: false,
	   configurable: false
	});	
	
	Object.defineProperty( that, "isEdge", {
	   value: true,
	   writable: false,
	   enumerable: false,
	   configurable: false
	});

	Object.preventExtensions(that);
	
	return that;
}

function graph(vertices, directed){
	"use strict";
	
	var i,
		that = {},
		printGraph, addVertex, findVertex, findVertexIndex, findEdgeIndex, removeVertex, addEdge, removeEdge, DFS, BFS, Dijkstra, Prim,
		vList = [],
		edges = {};
	
	findVertex = function(vLabel){
		var i;
		//alert("Looking for " + vLabel);
		for (i=0; i<vList.length; i++){
			//alert(vList[i].getLabel());
			if (vList[i].equals(vLabel) ){
				
				return vList[i];
			}
		}
		//else return undefined!
	};
	
	findVertexIndex = function(vLabel){	//Private: only for internal purpose;
		var i;
		//alert("Looking for " + vLabel);
		for (i=0; i<vList.length; i++){
			//alert(vList[i].getLabel());
			if (vList[i].equals(vLabel) ){
				
				return i;
			}
		}
		//else return undefined!
	};

	findEdgeIndex = function(srcLabel, destLabel){	//Private: only for internal purpose;
		var j;
		//alert("Looking for " + vLabel);
		for (j = 0; j<edges[srcLabel].length; j++){
			if ( edges[srcLabel] && edges[srcLabel][j].isEdge && edges[srcLabel][j].getDest().equals(destLabel) ){
				return j;	//It's not an hypergraph, so there can't be more edges to destLabel
			}
		}
		//else return undefined!
	};
	
	addVertex = function(vLabel){
		var v;
		if (findVertex(vLabel)){
			return null;
			//throw "Vertex already exists in the graph";
		}
		v = vertex(vLabel);
		vList.push(v);
		edges[vLabel] = [];
		return v;
	};
	
	removeVertex = function(vLabel){
		var srcLabel, j, i,
			id = findVertexIndex(vLabel);
		if (id === undefined){
			return false;
		}
		delete edges[vLabel];
		vList.splice(i,1);
		for (i = 0; i<vList.length; i++){
			srcLabel = vList[i].isVertex && vList[i].getLabel().toString();
			j = findEdgeIndex(srcLabel, vLabel);
			if (j !== undefined){
				edges[srcLabel].splice(j,1);
			}
		}
		return true;

	};
	
	addEdge = function(src, dest, weight){
		var vSrc = findVertex(src),
			vDest = findVertex(dest),
			e;
		if (!vSrc || !vDest){
			return null;
			//throw "At lest one vertex does not belong to the graph";
		}
		e = edge(vSrc, vDest, weight);
		edges[src].push( e );
		if (!directed){
			edges[dest].push( edge(vDest, vSrc, weight) );
		}
		return e;
	};
	
	removeEdge = function(srcLabel, destLabel){
		var id = findEdgeIndex(srcLabel, destLabel);
		if (id !== undefined){
			edges[srcLabel].splice(id,1);
			if (!directed){
				id = findEdgeIndex(destLabel, srcLabel);
				if (id !== undefined){
					edges[destLabel].splice(id,1);
				}
			}
			return true;
		}else{
			return false;
		}
	};
	
	DFS = function(){
		var i, j, predecessors = [], enter_time = [], exit_time = [], time = 0, vs = [], depthFirstSearch;
		for(i=0; i<vList.length; i++){
			if ( !vList.hasOwnProperty(i) || !vList[i].isVertex ){
				continue;
			}//else
			vList[i].color = "white";
//			predecessors[vList[i]] = undefined;
		}
		
		depthFirstSearch = function(vertex, parentLabel){
			var archi, i, e, vLabel;
//			if (!vertex || !vertex.isVertex){}//Already checked from the caller
			vLabel = vertex.getLabel();
			//Thanks, closure!
			if (parentLabel){
				e = edges[parentLabel][findEdgeIndex(parentLabel, vertex.getLabel())];	//Invariante: l'arco deve esistere (per i controlli precedenti)
				switch ( vertex.color  ){
					case "white":
						e.type = "tree";
						break;
					case "gray":
						e.type = "back";						
						return;
					case "black":
						if ( enter_time[vLabel] > enter_time[parentLabel] ){
							e.type = "forward";
						}else{
							e.type = "cross";
						}
						return;
					default :
						throw "Error";
				}
			}//else => vertex is a start one for DFS => color must be white (it is checked in the DS for loop)
			vertex.color = "gray";
			enter_time[vLabel] = ++time;
			predecessors[vLabel] = parentLabel;
			archi = edges[vLabel];
			for (i=0; i<archi.length; i++){
				if (!directed && archi[i].getDest().equals(parentLabel) ){
					//Undirect edges must be considered only once
					continue;
				}
				depthFirstSearch(archi[i].getDest(), vLabel);
			}
			exit_time[vLabel] = ++time;
		};
		
		for(i=0; i<vList.length; i++){
			if ( !vList.hasOwnProperty(i) || !vList[i].isVertex || vList[i].color !== "white" ){
				continue;
			}//else
			depthFirstSearch(vList[i]);			
		}
//<STAMPA>		
		for(i=0; i<vList.length; i++){
			if ( !vList.hasOwnProperty(i) || !vList[i].isVertex  ){
				continue;
			}//else
			vs.push( "<br/><br/>" + vList[i].getLabel() + " <= " + predecessors[vList[i].getLabel()] );
			for (j = 0; j<edges[vList[i].getLabel()].length; j++){
				if ( edges[vList[i].getLabel()][j].isEdge ){
					vs.push( " " + vList[i].getLabel() + " -> " + edges[vList[i].getLabel()][j].getDest().getLabel().toString() + ", " );
					if ( edges[vList[i].getLabel()][j].type ){
						vs.push( "(" + edges[vList[i].getLabel()][j].type + ")" );
					}
				}
			}
			
		}
//<STAMPA/>			
		return vs.join("");
	}

	BFS = function(sourceLabel){
		var s, v, u, i, vq, archi,
			predecessors = [],
			distances = [],
			vs = [];

		s = findVertex(sourceLabel);
		
		if (!s || !s.isVertex){
			throw "Illegal Argument: vertex not in graph";
		}
		
		for(i=0; i<vList.length; i++){
			if ( !vList.hasOwnProperty(i) || !vList[i].isVertex ){
				continue;
			}//else
			vList[i].color = "white";
			
//			predecessors[vList[i]] = undefined;
		}
		
		vq = priorityQueue();
		
		vq.push(node(sourceLabel,0));
		distances[sourceLabel] = 0;
		
		while (!vq.isEmpty()){
			
			v = vq.pop().key;
			
			//alert(v);
			archi = edges[v];
			//alert("L: " + archi.length);
			for(i=0; i<archi.length; i++){
				if (!archi.hasOwnProperty(i) || !archi[i].isEdge){
					continue;
				}
				u = archi[i].getDest().getLabel();
				if (  compareDistances(distances[v] + 1 , distances[u]  ) < 0 ){
					distances[u] = distances[v] + 1;
					predecessors[u] = v;
					if (!vq.decrease( u, distances[u]) ){
						vq.push( node(u), distances[u] ) ;
					}
				}
			}
		}
		
//<STAMPA>	
		vs.push("<br/><br/>Source = " + s.getLabel());
		for(i=0; i<vList.length; i++){
			if ( !vList.hasOwnProperty(i) || !vList[i].isVertex  ){
				continue;
			}//else
			v = vList[i].getLabel();
			vs.push( "<br/>" + v + " <= " + predecessors[v] + " d: "+ distances[v] );			
		}
		vs.push("<br/>");
//<STAMPA/>	

	return vs.join("");
		
	}
	
	Dijkstra = function(sourceLabel){
		var s, v, u, i, vq, archi,
			predecessors = [],
			distances = [],
			vs = [];

		s = findVertex(sourceLabel);
		
		if (!s || !s.isVertex){
			throw "Illegal Argument: vertex not in graph";
		}
		
		for(i=0; i<vList.length; i++){
			if ( !vList.hasOwnProperty(i) || !vList[i].isVertex ){
				continue;
			}//else
			vList[i].color = "white";
			
//			predecessors[vList[i]] = undefined;
		}
		
		vq = priorityQueue();
		
		vq.push(node(sourceLabel,0));
		distances[sourceLabel] = 0;
		
		while (!vq.isEmpty()){
			
			v = vq.pop().key;
			
			//alert(v);
			archi = edges[v];
			//alert("L: " + archi.length);
			for(i=0; i<archi.length; i++){
				if (!archi.hasOwnProperty(i) || !archi[i].isEdge){
					continue;
				}
				u = archi[i].getDest().getLabel();
				if (  compareDistances(distances[v] + archi[i].getWeight() , distances[u]  ) < 0 ){
					distances[u] = distances[v] + archi[i].getWeight();
					predecessors[u] = v;
					if (!vq.decrease( u, distances[u]) ){
						vq.push( node(u), distances[u] ) ;
					}
				}
			}
		}
		
//<STAMPA>	
		vs.push("<br/><br/>|Dijkstra|   Source = " + s.getLabel());
		for(i=0; i<vList.length; i++){
			if ( !vList.hasOwnProperty(i) || !vList[i].isVertex  ){
				continue;
			}//else
			v = vList[i].getLabel();
			vs.push( "<br/>" + v + " <= " + predecessors[v] + " d: "+ distances[v] );			
		}
		vs.push("<br/>");
//<STAMPA/>	

	return vs.join("");
		
	}	
	
	Prim = function(sourceLabel){
		var i, j , archi, srcLabel, destLabel, e,
			treeEdges = [], predecessors = [], treeVertex = [], vs = [],
			eq;
	
		if (vList.length<=0){
			throw "Graph is empty" ;
		}
		if (sourceLabel === undefined || sourceLabel === null || !findVertex(sourceLabel) ){
			do{
				i = Math.floor( vList.length * Math.random() );
			}while ( !vList.hasOwnProperty(i) );
			sourceLabel = vList[i].getLabel();
		}
		treeVertex[sourceLabel] = true;
		archi = edges[sourceLabel];
		
		eq = priorityQueue();
		for (i = 0; i < archi.length; i++){
			eq.push( node( archi[i], archi[i].getWeight() ) );
		}	
		
		while (!eq.isEmpty()){
			e = eq.pop().key;
			srcLabel = e.getSrc().getLabel();
			destLabel = e.getDest().getLabel();
			//treeVertex[srcLabel] ought to be true because of the way edges are added to the queue
			if ( !treeVertex[destLabel] ){
				//Add dest vertex to the tree
				treeVertex[destLabel] = true;
				predecessors[destLabel] = srcLabel;
				//Add the edge to the tree;
				treeEdges.push(e);
				//Add all edges from destLabel to non-tree vertices to the queue;
				archi = edges[destLabel];
				for (i = 0; i < archi.length; i++){
					if (!treeVertex[archi[i].getDest().getLabel()] ){
						eq.push( node( archi[i], archi[i].getWeight() ) );
					}
				}				
			}
		}
		
//<STAMPA>	
		vs.push( "<br/><br/>|PRIM|   Source: " + sourceLabel);
		for(i=0; i<vList.length; i++){
			if ( !vList.hasOwnProperty(i) || !vList[i].isVertex  ){
				continue;
			}//else
			vs.push( "<br/>" + vList[i].getLabel() + " <= " + predecessors[vList[i].getLabel()] );			
		}
		vs.push("<br/>--- Edges:");
		for (i = 0; i<treeEdges.length; i++){
			e = treeEdges[i];
			if ( e.isEdge ){
				vs.push( "<br/> " + e.getSrc().getLabel() + " -> " + e.getDest().getLabel() + " (" + e.getWeight() + ")" +  ", " );
			}
		}		
//<STAMPA/>			
		return vs.join("");		
	
	}

	printGraph = function(node){
		var vs = ["Vertices: "],
			es = ["Edges: "],
			i,j, srcLabel;
		for (i = 0; i<vList.length; i++){
			srcLabel = vList[i].isVertex && vList[i].getLabel().toString();
			vs.push( srcLabel );
			
			for (j = 0; j<edges[srcLabel].length; j++){
				es.push( edges[srcLabel][j].isEdge && ( srcLabel + " -> " + edges[srcLabel][j].getDest().getLabel().toString()  ) );
			}
		}
		node.innerHTML += "<br/><br/>" + vs.join(", ") + "<br/>" +  es.join(", ");
	};

	for (i=0; i<vertices.length; i++){
		addVertex(vertices[i]);
	}
	
	
	Object.defineProperty( that, "addEdge", {
	   value: 	addEdge,
	   writable: false,
	   enumerable: false,
	   configurable: false
	});

	Object.defineProperty( that, "removeEdge", {
	   value: 	removeEdge,
	   writable: false,
	   enumerable: false,
	   configurable: false
	});

	Object.defineProperty( that, "addVertex", {
	   value: addVertex,
	   writable: false,
	   enumerable: false,
	   configurable: false
	});
	
	Object.defineProperty( that, "findVertex", {
	   value: findVertex,
	   writable: false,
	   enumerable: false,
	   configurable: false
	});

	Object.defineProperty( that, "removeVertex", {
	   value: removeVertex,
	   writable: false,
	   enumerable: false,
	   configurable: false
	});

	Object.defineProperty( that, "print", {
	   value: printGraph,
	   writable: false,
	   enumerable: false,
	   configurable: false
	});
	
	Object.defineProperty( that, "printDFS", {
	   value: function(console){
			console.innerHTML += DFS();
	   },
	   writable: false,
	   enumerable: false,
	   configurable: false
	});

	Object.defineProperty( that, "printBFS", {
	   value: function(source, console){
			console.innerHTML += BFS(source);
	   },
	   writable: false,
	   enumerable: false,
	   configurable: false
	});

	Object.defineProperty( that, "printDijkstra", {
	   value: function(source, console){
			console.innerHTML += Dijkstra(source);
	   },
	   writable: false,
	   enumerable: false,
	   configurable: false
	});


	Object.defineProperty( that, "printPrim", {
	   value: function(source, console){
			console.innerHTML += Prim(source);
	   },
	   writable: false,
	   enumerable: false,
	   configurable: false
	});

	
	Object.preventExtensions(that);

	return that;	
}

function compareDistances(d1, d2){
	if (d1 === undefined){
		if ( d2 === undefined ){
			return 0;
		}else{
			return 1;
		}
	}else{
		if ( d2 === undefined ){
			return -1;
		}else{
			return d1 - d2;
		}								
	}
}

/*
var vertices = ["1", "A", "C", "pippo"];
var G = graph(vertices, false);
G.addEdge("1", "A",4);
//G.print(getConsole());
G.addVertex("azz");
G.addEdge("C", "azz",4);
*/
var vertices = ["A", "B", "C", "E", "F", "H", "K", "Goal"];
var G = graph(vertices, true);
G.addEdge("A", "B",2);
G.addEdge("A", "C",6);
G.addEdge("A", "Goal",750);
G.addEdge("B", "C",30);
G.addEdge("B", "E",2);
G.addEdge("C", "Goal",750);
G.addEdge("E", "C",35);
G.addEdge("E", "F",1);
G.addEdge("E", "Goal",1);
G.addEdge("E", "K",3);
G.addEdge("F", "C",1);
G.addEdge("K", "H",6);
G.addEdge("H", "E",7);
G.addEdge("H", "B",5);
G.print(getConsole());
G.printDFS(getConsole());
G.printBFS("A",getConsole());
G.printDijkstra("A",getConsole());
G.printPrim("A",getConsole());
G.removeVertex("1");
//G.print(getConsole());
G.removeEdge( "azz", "C");
G.print(getConsole());