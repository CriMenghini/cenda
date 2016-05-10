# -*- coding: utf-8 -*-
"""
Created on Tue May 10 15:09:06 2016

@author: michele
"""

from library import *

tipo1 = 1==int(raw_input("Would you like to use: \n 1: Random Graph(n,p) \n 2: Regular Random Graph (n,m) \n [1/2]: "))


n=int(raw_input('\nNumber of node? (Suggested less then 250, unless the computation of eigenvalues will be slow)\n'))


if tipo1: 
    p= float( raw_input('Probability p :'))
    g=r_graph(n,p)
else: 
    m= int(raw_input('Number of edges per node m :'))
    show= 1==int(raw_input('Do you want to see the evolution of the graph during the algorithm? \n 1:yes\n 2:no\n' ))
    g=r_graph_regular(n,m,show)

 #random graph: viene sempre connesso
g = r_graph(100)

#grafo esempio 
G=nx.Graph()

da = int(0)
a = int(1)
G.add_edge(da,a)

da = int(1)
a = int(2)
G.add_edge(da,a)

#se aggiungi questo
'''da = int(2)
a = int(3)
G.add_edge(da,a)'''

da = int(3)
a = int(4)
G.add_edge(da,a)

#e questo viene un anello
'''da = int(4)
a = int(0)
G.add_edge(da,a)'''

#altrimenti è sconnesso

#basta aggiungere un arco e viene connesso

#stampo con metodo michele grafo esempio
print_graph(G)

print "testing connectivity of graphs.."
print ''

print "algebraic method 1 (irreducibility)"
print "is the random graph connected:", testConnectIrredA(g)
print "is the example graph connected:", testConnectIrredA(G)
print ''

print "algebraic method 2 (eigenvalue of the Laplacianmatrix)"
print "is the random graph connected:", testConnectLapEig(g)
print "is the example graph connected:", testConnectLapEig(G)
print ''

print "breadth-first based algorithm"
print "is the random graph connected:", testConnectBFS(g)
print "is the example graph connected:", testConnectBFS(G)
