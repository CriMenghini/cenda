# -*- coding: utf-8 -*-
"""
Created on Tue May 10 15:09:06 2016

@author: michele
"""

from library import *
from fatTree import *

## prima domanda al prof.
#tipo1 è una variabile booleana, true se dice che vuole solo random_graph(n,p false se vuole il regular_random_graph)
tipo1 = 1==int(raw_input("Would you like to use: \n 1: Random Graph(n,p) \n 2: Regular Random Graph (n,m) \n [1/2]: "))

#nodi
n=int(raw_input('\nNumber of node? (Suggested less then 250, unless the computation of eigenvalues will be slow)\n'))


if tipo1: 
    #probabilità    
    p= float( raw_input('Probability p :'))
    #crea il grafo random e lo associa a g    
    g=r_graph(n,p)
else: 
    #nuemro di edge per nodi    
    m= int(raw_input('Number of edges per node m :'))
    #show è booleana, è true se vuole vedere l'evoluzione dei graphi    
    show= 1==int(raw_input('Do you want to see the evolution of the graph during the algorithm? \n 1:yes\n 2:no\n' ))
    g=r_graph_regular(n,m,show)


ins = int(raw_input('\n 0: Perform the BFS only for one node type 0\n 1: Perform the algorithm on each node\n [0/1]: '))

#compute the adiacence matrix as a dict 
Adj = {n : g.neighbors(n) for n in g.nodes()}

if ins == int(0):
    print '\n \n BFS performed on root = 2'
    print BFS(2,Adj)
else:
    print '\n \n BFS performed on each node of the graph'
    graphs = pd.DataFrame.from_dict(BFS_all_nodes(g.nodes(), Adj), orient = 'index')
    graphs[graphs.isnull()]=-1
    graphs[(graphs==-1)]='inf'
    print graphs

root = int(raw_input('\n Choose a root( between 0 and the number of nodes-1) to perform the BFS algorithm and draw the obtained graph:'))

graphs = pd.DataFrame.from_dict(BFS_all_nodes(g.nodes(), Adj))
graphs[graphs.isnull()]=-1
print_bfs(g.nodes(), root , Adj, graphs)

print "testing connectivity of graphs.."
print ''
print '-----------------------------------'
print "algebraic method 1 (irreducibility)"
print "is the random graph connected:"
print testConnectIrredA(g)
print ''
print '-----------------------------------'
print "algebraic method 2 (eigenvalue of the Laplacianmatrix)"
print "is the random graph connected:"
print testConnectLapEig(g)
print ''
print '-----------------------------------'
print "breadth-first based algorithm"
print "is the random graph connected:"
print testConnectBFS(g)

op=int(raw_input('\nType:\n 0: To see the FatTree implementation \n 1: To stop \n '))

if op == 0:
    main()
else:
    print 'Cenda thanks you. Goodbye!'

print 'Cenda thanks you. Goodbye!'
