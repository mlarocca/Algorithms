from sys import argv
from random import randrange
from copy import copy, deepcopy
from union_find import UnionFind

def contract(G, edges, cuts, edges_index):
    m = len(edges)
    while True:
        u, v = edges[edges_index]
        edges_index += 1
        v = cuts.find_root(v)
        u = cuts.find_root(u)
        if not cuts.connected(u, v):
            break
    cuts.union(u, v)

    w = cuts.find_root(u)    #find the common root of the two vertices

    if w != v:
        for k, z in G.get(v, []):
            #print z, v
            if not cuts.connected(z, v):
                G[w].append((k, z))
        del G[v]

    if w != u:
        for k, z in G.get(u, []):
            #print z, u
            if not cuts.connected(z, u):
                G[w].append((k, z))
        del G[u]

    #G[w] = filter(lambda (k, z): not cuts.connected(w, z), G[w])

    return edges_index

def karger_min_cut(G, edges):

    n = max(G.keys())
    cuts = UnionFind(n+1)

    edges_map = {}
    edges_index = 0
    for _ in xrange(n-2):
        edges_index = contract(G, edges, cuts, edges_index)
        #print G, edges

    assert(len(G) == 2)
    u, v = G.keys()
    #assert(len(G[u]) == len(G[v]))

    #before returning the cuts list, we must remove the self loops from the adjacency list 
    return filter(lambda (k, z): not cuts.connected(u, z), G[u])   #each edge is stored twice, so we can just return one of the two vertices' adj list


def montecarlo_karger(G, edges, N):
    min_cut_len = float('inf')
    min_cut = []

    m = len(edges)
    for _ in xrange(N):
        G_1 = deepcopy(G)
        #shuffle edges, to mimic random edge selection, but in a faster way
        for i in xrange(m):
            j = randrange(i, m)
            tmp = edges[j]
            edges[j] = edges[i]
            edges[i] = tmp

        mc = karger_min_cut(G_1, edges)
        if len(mc) < min_cut_len:
            min_cut_len = len(mc)
            min_cut = mc
            print min_cut
    return min_cut

def read_input(f):
    G = {}
    edges = []
    for line in f:
        line = map(int, line.strip().split(" "))
        v = line[0]
        G[v] = map(lambda u: (v,u), line[1:])
        for i in xrange(1, len(line)):
            edges.append((v, line[i]))
    f.close()
    return G, edges    

if __name__ == "__main__":
    G, edges = read_input(open(argv[1], 'r'))

    min_cut = montecarlo_karger(G, edges, len(G) )
    print len(min_cut), min_cut