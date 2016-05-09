# -*- coding: utf-8 -*-


import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from numpy import linalg as LA

def r_graph(n=10,p=0.3):
    adj=np.random.choice([1,0],[n,n],p)
    np.fill_diagonal(adj,1)
    adj=adj*(adj.T)
    g=nx.from_numpy_matrix(adj)
    print_graph(g)
    return g
    
#G (n,m) model:

#n number of nodes
#m degree of regularity of the graph ( each node has exactly m edges)
#show if you want to check the progression of the constructor
def r_graph_regular(n=10,m=2,show=True):
    g=nx.Graph()
    g.add_nodes_from(range(n))
    for iteration in range(m):
        permutation=np.random.permutation(range(n)) 
        to_connect1=permutation[:(n/2)]  
        to_connect2=permutation[(n/2):]  
        links=zip(to_connect1,to_connect2)
        g.add_edges_from(links)
        checked=set()
        if show:print_graph(g)
        for (i,j) in g.degree().items():
            
            if j<iteration+1:
                if i in checked:
                    continue
                if i in to_connect1:
                    k=to_connect2[to_connect1==i].item()
                else: k=to_connect1[to_connect2==i].item()
                h,l=g.edges()[np.random.randint(g.number_of_edges())]
                while h==i or l==i or h in g[i].keys() or l in g[k].keys() :
                     h,l=g.edges()[np.random.randint(g.number_of_edges())]
                
                if show:print_graph(g,special=True,old_new=[h,l,i,k])                
                g.add_edge(h,i)
                g.add_edge(l,k)
                g.remove_edge(h,l)
                checked.add(k)
                checked.add(i)
                
    print g.degree()
    return g
    
def print_graph(g, special=False,old_new=[]):
    pos=nx.spring_layout(g)
    nx.draw_networkx_nodes(g,pos,node_color='r',
                           node_size=500,
                       alpha=0.8)
    labels={i:i for i in range(g.number_of_nodes())}
    nx.draw_networkx_labels(g,pos,labels,font_size=16)
    if special:
        nx.draw_networkx_edges(g,pos,edgelist=[(old_new[0],old_new[1]),(old_new[0],old_new[2]),(old_new[1],old_new[3])],edge_color=['r','b','b'],width=3.0,alpha=0.5)
    nx.draw_networkx_edges(g,pos,width=1.0,alpha=0.5)
    plt.show(block=False)
	
def BFS(root, adjecency_list):
	"""This function returns a dictionary whose keys are the nodes and the values are the respective 
	distances from the root.
	- root : is the departure node
	- adjecency_list : is a dictionary whose keys are the node of the graph and the respective value is the list of 
	neighbors"""
		
	# Initialize the dictionary of level
	level = { root : 0 }
	# Define the dictionary of parents {node : {set of parents}}
	parent = { root : set()}

	# Counter 'i' for the search level
	i = 1

	# Define the frontiers as the list of nodes that we reach in the previous step( respect i-1 level)
	frontier = [root]

	# Loop
	while frontier != []:
		
		# Get the list of nodes in the frontier
		level_keys = level.keys()
		# Initialize the new frontier list as empty
		next = [] 
		
		# For each node in the frontier that corresponds to level i-1
		for u in frontier:
			# For each node in the adjecency list of u
			for v in adjecency_list[u]:
				# If the node has not already been discovered
				if v not in level_keys:
					# Add it in the level dictionary
					level[v] = i
					# define u as ita parent
					parent[v] = u
					# And append it to the new level frontier
					next.append(v)
		frontier = next
		
		# Next level
		i += 1

	return level

	
def testConnectLapEig(g):
    n = len(g.nodes())
    L = np.zeros((n,n))
    for x,i in g.edges():
        L[x,i] = -1
        L[i,x] = -1
    for x in g.nodes():
        L[x,x] = g.degree(x)
    w, v = LA.eig(L)
    seconSmallestEig = sorted(list(w))[1]
    return seconSmallestEig > 0
    
	
def testConnectIrredA(g):
    n = len(g.nodes())
    A = np.zeros((n,n))
    for x,i in g.edges():
        A[x,i] = 1
        A[i,x] = 1
    somma = np.identity(n)
    for x in range(1,n):
        somma = LA.matrix_power(A, x) + somma
    boolean = True
    for i in range(0,n):
        for j in range(0,n):
            boolean = boolean and somma[i,j] > 0
	return boolean
	
	
def testConnectBFS(g):
    Adj = {n : g.neighbors(n) for n in g.nodes()}
    level = BFS(g.nodes()[0], Adj)
    return len(level.keys()) == len(g.nodes())	
	
	

g = r_graph(100)

G=nx.Graph()

da = int(0)
a = int(1)
G.add_edge(da,a)

da = int(1)
a = int(2)
G.add_edge(da,a)

'''da = int(2)
a = int(3)
G.add_edge(da,a)'''

da = int(3)
a = int(4)
G.add_edge(da,a)

'''da = int(4)
a = int(0)
G.add_edge(da,a)'''

print_graph(G)

print "testing connectivity of graphs.."
print ''

print "algebraic method 1 (irreducibility)"
print "is the random graph connected:", testConnectIrredA(g)
print "is the disconnected graph connected:", testConnectIrredA(G)
print ''

print "algebraic method 2 (eigenvalue of the Laplacianmatrix)"
print "is the random graph connected:", testConnectLapEig(g)
print "is the disconnected graph connected:", testConnectLapEig(G)
print ''

print "breadth-first based algorithm"
print "is the random graph connected:", testConnectBFS(g)
print "is the disconnected graph connected:", testConnectBFS(G)
