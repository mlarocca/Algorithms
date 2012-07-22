function queue(){
	"use strict";
	
	var top = 0, bottom = -1, coda = [], that = {};
	
	Object.defineProperty( that, "isEmpty", {
	   value: function(){
				return (bottom < top);
				},
	   writable: false,
	   enumerable: false,
	   configurable: false
	});
	
	Object.defineProperty( that, "push", {
	   value: function(el){
				coda[bottom] = el;
				bottom += 1;
				},
	   writable: false,
	   enumerable: false,
	   configurable: false
	});

	Object.defineProperty( that, "top", {
	   value: function(){
				if (bottom >= top){
					return coda[top];
				}
			},
	   writable: false,
	   enumerable: false,
	   configurable: false
	});

	Object.defineProperty( that, "pop", {
	   value:	function(){
					var el;
					if (bottom >= top){
						el = coda[top];
						delete coda[top];
						top += 1;
					}
					
					return el;
			},
	   writable: false,
	   enumerable: false,
	   configurable: false
	});

	Object.preventExtensions(that);
	return that;
}

function priorityQueue(){
	"use strict";
	var top = 1, bottom = 0, coda = [], that = {};
	
	Object.defineProperty( that, "isEmpty", {
	   value: function(){
				return (bottom < top);
				},
	   writable: false,
	   enumerable: false,
	   configurable: false
	});
	
	Object.defineProperty( that, "push", {
	   value:	function(el){
					var i, parent, tmp;
					if ( !el || !el.hasOwnProperty("key") || !el.hasOwnProperty("compareTo") || typeof el.compareTo != 'function'){
						throw "Illegal argument: the element must have a key and be comparable";
					}
					bottom += 1;
					coda[bottom] = el;
					for (i = bottom; i>top;  ){
						parent = top + Math.floor( ( i - top ) / 2);
						//alert(i + " | " + parent);
						if ( coda[parent].compareTo(coda[i]) > 0 ){
							tmp = coda[parent];
							coda[parent] = coda[i];
							coda[i] = tmp;
						}else{
							break;
						}
						i = parent;
					}
				},
	   writable: false,
	   enumerable: false,
	   configurable: false
	});	

	Object.defineProperty( that, "decrease", {
	   value:	function(key, newVal){
					var i, parent, tmp;
					for (i=top; i<=bottom; i++){
						if ( coda[i].key === key ){
							break;
						}
					}
					if (i>bottom){
						return false; //Element not found;
					}
					
					coda[i].val = newVal;
					for (; i>top;  ){
						parent = top + Math.floor( ( i - top ) / 2);
						//alert(i + " | " + parent);
						if ( coda[parent].compareTo(coda[i]) > 0 ){
							tmp = coda[parent];
							coda[parent] = coda[i];
							coda[i] = tmp;
						}else{
							break;
						}
						i = parent;
					}
					return true;	//Element found
				},
	   writable: false,
	   enumerable: false,
	   configurable: false
	});	

	Object.defineProperty( that, "top", {
	   value: function(){
				if (bottom >= top){
					return coda[top];
				}
			},
	   writable: false,
	   enumerable: false,
	   configurable: false
	});

	Object.defineProperty( that, "pop", {
	   value:	function(){
					var el, i, j, tmp;
					if (bottom >= top){
						el = coda[top];
						coda[top] = coda[bottom];
						delete coda[bottom];
						bottom -= 1;
						i = top;
						j = top + 1;
						while (j <= bottom){
							if (j+1 <= bottom && coda[j].compareTo(coda[j+1]) > 0 ){
								j += 1;
							}
							if ( coda[i].compareTo(coda[j]) <= 0 ){
								break;
							}else{
								tmp = coda[i];
								coda[i] = coda[j];
								coda[j] = tmp;
								i = j;
								j = top + (j-top) * 2;
							}
						}
						
					}
					
					return el;
			},
	   writable: false,
	   enumerable: false,
	   configurable: false
	});

	Object.defineProperty( that, "toString", {
	   value:	function(){
					var i, arr=[];
					//alert(top + " " + bottom);
					for(i=top; i<=bottom; i++){
						arr.push(coda[i].key);
					}
					return arr.join();
				},
	   writable: false,
	   enumerable: false,
	   configurable: false
	});
	
	Object.preventExtensions(that);
	return that;
	
}


/*
var PQ = priorityQueue();
PQ.push(node(4));
PQ.push(node(3));
PQ.push(node(5));
PQ.push(node(2));
PQ.push(node(1));
PQ.push(node(0));
PQ.push(node(-2));

//alert("PQ");
getConsole().innerHTML += "<br/>" + PQ.toString();
while(!PQ.isEmpty()){
	alert( PQ.pop().key);
	getConsole().innerHTML += "<br/>" + PQ.toString();
}
*/