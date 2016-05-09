# -*- coding: utf-8 -*-
"""
Created on Mon May  9 17:38:44 2016

@author: cristinamenghini
"""

import networkx as nx

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
    
    
# Example 

# Define the graph
G = nx.Graph()
# List of nodes
nodes = ['a','z','s','x','d','c','v','f']
# Add nodes to the graph
G.add_nodes_from(nodes)
# List of edges
edges = [('a','z'),('a','s'),('x','s'),('x','d'),('x','c'),('d','f'),('c','f'),('f','v'),('c','v')]
# Add edges to the graph
G.add_edges_from(edges)

# Define the dictionary {node : list of neighbors}
Adj = {n : G.neighbors(n) for n in nodes}

# Apply the algorithm respect to root 's'
BFS('s', Adj)

# If you want to do the exploration definig as root each different node of the graph
res = {}
for n in nodes:
    res[n] = BFS(n, Adj)