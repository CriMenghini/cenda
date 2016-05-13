# -*- coding: utf-8 -*-
"""
Created on Tue May 10 14:57:22 2016

@author: michele
"""

# -*- coding: utf-8 -*-


import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from numpy import linalg as LA
from scipy.sparse import dok_matrix
import pandas as pd
from random import randint
import time

def r_graph(n=10,p=0.3):
    adj=np.random.choice(2,[n,n],p=[1-np.sqrt(p),np.sqrt(p)])
    np.fill_diagonal(adj,0)
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
    if not show:print_graph(g)    
    print ' Graph with ', n, ' nodes,', m, ' edges for each node', '\nCheck degree of nodes, {i:k} , i is the node, k is the degree'            
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
    plt.show()
   
def prob_connectivity(n,p):
    
    import sympy as sy
    
    def disc_prob_n (n,p,connection):
        a=0
        for i in range(1,n):
            a+= connection[i]*sy.binomial(n-1,i-1)*(1-p)**(i*(n-i))
        return a
    
    def con_prob_n (n,p):
        connection={}
        connection[1]=1
        for i in range(2,n+1):
            connection[i]=1-disc_prob_n(i,p,connection)
        return connection[n]
        
    import numpy as np
    import matplotlib.pyplot as plt
    
    f=np.vectorize(con_prob_n)
    x=np.arange(0.015,0.1,0.005)
    y=f(n,p=x)
    
    x0=x[y>0.99][0]
    y0=y[y>0.99][0]
    plt.plot(x,y,'-',linewidth=3)
    plt.ylim(0,1)
    plt.yticks([0.99]+list(np.arange(0,1,0.1)))
    plt.xticks(list(np.arange(0,0.1,0.01)))
    plt.xlabel('p of existing for each possible edge')
    plt.ylabel('p for the graph to be connected')
    plt.title('P{ Random Graph(n,p) is connected }',size=20,color='darkred',y=1.08)
    plt.plot([x0,x0],[0,y0],'k-',color='r')
    plt.plot([0,x0],[y0,y0],'k-',color='r')
    plt.plot(x0,y0,'o',linewidth=3, color='r')
    plt.show()
	
def BFS(root, adjecency_list):
    """This function returns a dictionary whose keys are the nodes and the values are the respective 
    distances from the root.
    - root : is the departure node
    - adjecency_list : is a dictionary whose keys are the node of the graph and the respective value is the list of 
    neighbors"""
        
    # Initialize the dictionary of level
    level = { root : 0 }
    # Define the dictionary of parents {node : {set of parents}}
    parent = { root : root}
    
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
    
    return level, parent
    
def BFS_all_nodes(list_node, ad_list):
    """This function return the depth of each node respect to different roots.
    - list_node is the list of nodes
    - ad_list is is a dictionary whose keys are the node of the graph and the respective value is the list of 
    neighbors"""
    depth = {}
    # For each node perform the BFS algorithm
    for n in list_node:
        if len(ad_list[n]) == 0:
            depth[n] = {k:-1 for k in range(len(list_node))}
        else:
            depth[n] = BFS(n, ad_list)[0]
    
    return depth

def create_edges(node, adj_list, df):
    """This function returns the dictionary {root : list of edges}.
    - node is the list of nodes;
    - adj_list is a dictionary whose keys are the node of the graph and the respective value is the list of 
    neighbors;
    - df is the dataframe that contains the result of BFS for each node."""

    # Initialize the return of the function    
    edges_list = {}
    # For each node
    for n in node:
        edges_list[n] = []
        # Get the max depth
        maxim = int(df[n].max(0,skipna=True))
        # Its parent
        parents = BFS(n, adj_list)[1]
        # And the create the edges
        for i in range(maxim+1):
            next_step = df[df[n] == i].index.tolist()
            for ns in next_step:
                edges_list[n].append((parents[ns], ns))
    
    return edges_list

def print_bfs(nods, rt, adj, data ):
    """This function draw the graph related to each different root.
    - nods is the list of all nodes of the graph;
    - rt is the root;
    - adj is is a dictionary whose keys are the node of the graph and the respective value is the list of 
    neighbors;
    - data is the dataframe that contains the result of BFS for each node."""
    
    # Define the empty graph
    G = nx.Graph()
    # Add nodes to the graph
    G.add_nodes_from(nods)
    # List of edges
    G.add_edges_from(create_edges(nods, adj, data)[rt])
    
    pos=nx.spring_layout(G)
    # Draw the graph
    #nx.draw(G, pos, with_labels = True)
    levels = BFS(rt, adj)[0]
    maxs = int(data[rt].max(0)) 
    #print maxs
    colors = ['#%06X' % randint(0, 0xFFFFFF) for i in range(10000)]  
    nx.draw_networkx_nodes(G,pos,
                       nodelist=[rt],
                       node_color= 'r',
                       node_size=500, alpha = 0.8)
    nod = [i for i in levels.keys()]
    for i in range(1,maxs+1):
        nx.draw_networkx_nodes(G,pos,
                       nodelist=[k for k in nod if levels[k] == i],
                       node_color= colors[i],
                       node_size=500, alpha = 0.8)
        #except:
            #continue
    
    nx.draw_networkx_edges(G,pos,
                       edgelist=create_edges(nods, adj, data)[rt],
                       width=2)
    labels = {n : n for n in nods}
    nx.draw_networkx_labels(G,pos,labels,font_size=16)
    plt.show()


#funzione per trovare connettività con matrice di adiacenza sparse
def testConnectIrredA(g):
	begin = time.time()
	print ''
	print '-----'
	n = len(g.nodes())
	A = dok_matrix((n,n), dtype=float)
	for x,i in g.edges():
		if x != i :
			A[x,i] = 1
			A[i,x] = 1
	somma = np.identity(n)
	print 'Computing matrix equal to: I + sum(A^x)..'
	for x in range(1,n):
		somma = A**x + somma
	boolean = True
	print 'Checking if the matrix computed is positive..'
	for i in range(0,n):
		for j in range(0,n):
			boolean = boolean and somma[i,j] > 0
	print ''
	print 'elapsed time:', time.time() - begin,' s'
	print ''
	if boolean:
		print 'Every value of the computed matrix is positive,'
		print 'then the graph is connected'
		print '-----'
		return True
	else:
		print 'The computed matrix is not totally positve,'
		print 'then the graph is disconnected'
		print '-----'
		return False
	

#funzione per trovare connettività con laplaciana
def testConnectLapEig(g):
	begin = time.time()
	print ''
	print '-----'
	print 'Computing eigenvalues of L..'
	n = len(g.nodes())
	L = np.zeros((n,n))
	for x,i in g.edges():
		L[x,i] = -1
		L[i,x] = -1
	for x in g.nodes():
		if (x,x) in g.edges():
			L[x,x] = g.degree(x)-2
		else:
			L[x,x] = g.degree(x)
	w, v = LA.eig(L)
	w = sorted(list(w))
	print ''
	print 'elapsed time:', time.time() - begin,' s'
	print ''
	print 'the eigenvalues of L are:'
	c = 0
	for x in w:
		if np.iscomplex(x):
			print 'Complex eigenvalue:',x
		else:
			print float(np.where(x < 1e-10, 0, x))
		c = c + 1
		if c == 4:
			print 'and more..'
			break

	if np.iscomplex(w[1]):
		print ''
		print 'the second smallest eigenvalue is complex:', w[1]
		print ''
		seconSmallestEig = np.real(w[1])
	else:
		seconSmallestEig = float(np.where(w[1] < 1e-10, 0, w[1]))
		print ''
		print 'the second smallest eigenvalue is:', seconSmallestEig
		print ''
	
	if seconSmallestEig > 0 :
		print 'which is positive: the graph is connected'
		print '-----'
		return True
	else:
		print 'which is negative: the graph is disconnected'
		print '-----'
		return False
	
		


#funzione per trovare connettività con BFS	
	
def testConnectBFS(g):
	begin = time.time()
	Adj = {n : g.neighbors(n) for n in g.nodes()}
	level = BFS(g.nodes()[0], Adj)[0]
	print ''
	print '-----'
	print '# of explored nodes', len(level.keys())
	print '# of total nodes', len(g.nodes())
	boool = len(level.keys()) == len(g.nodes())
	print ''
	print 'elapsed time:', time.time() - begin,' s'
	print ''
	if boool:
		print 'the graph is connected since we have explored all nodes'
		print '-----'
		return True
	else:
		print "the graph is disconnected since we didn't reach all nodes"
		print '-----'
		return False
	
