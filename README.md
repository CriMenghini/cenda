# cenda

Some graph models and algorithms to be applied on Data Center topology

#### Contents

* PART 1 : generate Erdos-Renyi graph with 
  - G(n,m) model : a graph is chosen uniformly at random from the collection of all graphs which have n nodes and m edges;
  - G(n,p) model : a graph is constructed by connecting nodes randomly. Each edge is included in the graph with probability p independent from every other edge. 

* PART 2 : BFS.py 
 - Implement the breadth-first search for all nodes of the graph;
 - Define the function to create a different graph for each different node choosen as root;
 - Draw the graph related to a specific root.

* PART 3 : Connectivity
 - algebraic method 1 (irreducibility);
 - algebraic method 2 (eigenvalue of the Laplacianmatrix);
 - breadth-first based algorithm.

* PART 4 : Fat Tree 
 - Generate a fat tree topology graph 
 - Find all paths connecting a given source ToR and a given destination ToR.
 - Find all disjoint paths connecting a given source ToR and a given destination ToR.

