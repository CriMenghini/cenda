# -*- coding: utf-8 -*-
"""
Created on Mon May  9 17:38:44 2016

@author: cristinamenghini
"""

import networkx as nx		
import pandas as pd
from random import randint

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
    
    return level, parent
    
def BFS_all_nodes(list_node, ad_list):
    """This function return the depth of each node respect to different roots.
    - list_node is the list of nodes
    - ad_list is is a dictionary whose keys are the node of the graph and the respective value is the list of 
    neighbors"""
    
    depth = {}
    # For each node perform the BFS algorithm
    for n in list_node:
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
        maxim = df[n].max(0)
        # Its parent
        parents = BFS(n, adj_list)[1]
        # And the create the edges
        for i in range(1, maxim+1):
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
    maxs = data[rt].max(0) 
    colors = ['#%06X' % randint(0, 0xFFFFFF) for i in range(10)]  
    nx.draw_networkx_nodes(G,pos,
                       nodelist=[rt],
                       node_color= 'r',
                       node_size=500, alpha = 0.8)
    for i in range(1,maxs+1):
        nx.draw_networkx_nodes(G,pos,
                       nodelist=[k for k in nodes if levels[k] == i],
                       node_color= colors[i],
                       node_size=500, alpha = 0.8)
    
    nx.draw_networkx_edges(G,pos,
                       edgelist=create_edges(nods, adj, data)[rt],
                       width=2)
    labels = {n : n for n in nods}
    nx.draw_networkx_labels(G,pos,labels,font_size=16)
    
    
    
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

# Create a dataframe whose each point value (i,j) is the depth of j respect root i.(the matrix is symmetric) 
graphs = pd.DataFrame.from_dict(BFS_all_nodes(nodes, Adj))

# Print the graph for a specific root
print_bfs(nodes, 'a', Adj, graphs)

