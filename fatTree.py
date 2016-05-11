# -*- coding: utf-8 -*-
"""
Created on Mon May  9 16:48:25 2016

@author: aalto
"""

import networkx as nx
import matplotlib.pyplot as plt
import pylab

''' This program generates a fat tree given in input the number of ports the user would like
    to have on each switch of the network. Than after generating the fat tree, the program
    is able to compute all the shortest paths between any pair of edge switches and also 
    all the disjoint shortest path between any pair of edges switches '''

def generatePod(k, numPod):
    ''' The POD is the fundamental block of a fat tree. Each POD is composed by k number of switches
        each one with k ports. We have k/2 aggregation switches and k/2 edge switches. Between
        the two types of switches we have a bipartite interconection structure where each
        edge-switch is connected to each aggreate-switch. Then each edge-switch is connected
        to k/2 servers and each aggregate-switch is connected to k/2 core switch'''
        
    pod = nx.Graph()
    aggregateLayer = nx.Graph()
    aggregateSwitches1 = map(lambda z: ("a"+str(numPod)+str(z),{"type":"aggregate1"}),range(0,k/4))
    aggregateSwitches2 = map(lambda z: ("a"+str(numPod)+str(z),{"type":"aggregate2"}),range(k/4,k/2))
    aggregateLayer.add_nodes_from(aggregateSwitches1)
    aggregateLayer.add_nodes_from(aggregateSwitches2)
    edgeLayer = nx.Graph()
    edgeSwitches = map(lambda z: ("e"+ str(numPod)+str(z),{"type":"edge"}),range(0,k/2))
    edgeLayer.add_nodes_from(edgeSwitches)
    for switchA in aggregateLayer.nodes(data=True):
        pod.add_node(switchA[0],switchA[1])
        for switchE in edgeLayer.nodes(data=True):
            pod.add_node(switchE[0],switchE[1])
            pod.add_edge(switchA[0], switchE[0])
    return pod
    
def generateFatTree(k):
    ''' A fat tree is composed by k PODs. Each POD is connected to all the core switches by
        means of the aggregate-switches: each one of those is connected to k/2 core switches '''
        
    fatTree = nx.Graph()
    cores = map(lambda z: ("c"+str(z),{"type":"core"}),range(0,k^2/4))
    fatTree.add_nodes_from(cores)
    pods = [generatePod(k, z) for z in range(0,k)]
    for pod in pods:
        fatTree = nx.union(fatTree, pod)
        for node in pod.nodes(data=True):
            if node[1]["type"] == "aggregate1":
                fatTree.add_edges_from([(node[0],core[0]) for core in cores[0:k/2]])
            elif node[1]["type"] == "aggregate2":
                fatTree.add_edges_from([(node[0],core[0]) for core in cores[k/2:k]])
                
    return fatTree

    
def dijkstra_all_shortest_paths(G, source, target, weight=None):
    ''' This function is the networkX's implementation of the "all-shortest-paths-problem" algorithm
        and is used as ground truth for our implementation. It uses a modified version of the 
        dijkstra algorithm that compute  the shortest path length and predecessors 
        on shortest paths.'''
        
    if weight is not None:
        pred,dist = nx.dijkstra_predecessor_and_distance(G,source,weight=weight)
    else:
        pred = nx.predecessor(G,source)
    if target not in pred:
        raise nx.NetworkXNoPath()
    stack = [[target,0]]
    top = 0
    while top >= 0:
        node,i = stack[top]
        if node == source:
            yield [p for p,n in reversed(stack[:top+1])]
        if len(pred[node]) > i:
            top += 1
            if top == len(stack):
                stack.append([pred[node][i],0])
            else:
                stack[top] = [pred[node][i],0]
        else:
            stack[top-1][1] += 1
            top -= 1
            
def disjointPaths(G, k, source, target):
    ''' The disjoint shortest paths are the ones that do not have any common edge or vertex,
        with the exception of the source and the target, here we compute those path in a naive
        way concatenate the neighbours of the source with the neighbours of the target by means
        of the common core-switches '''
        
    paths = {}
    firstPath = [[source,aggS] for aggS in G.neighbors(source)]
    secondPath = [[aggT,target] for aggT in G.neighbors(target)]
    if source[1]==target[1]:
        paths = map(lambda node: [source,node,target], G.neighbors(source))
    else:
        for x in range(0,k/2):
            if x < k/4:
                paths[x] = firstPath[x] + ["c"+str(x)] + secondPath[x]
            else:
                paths[x] = firstPath[x] + ["c"+str(x+k/2)] + secondPath[x]
    return paths
    
def allShortestPaths(G, k, source, target):
    ''' We compute the shortest paths between two elements by iterating over the neighbors at
        each level: edge, aggregate and core. We use the labeling used during the creation
        of the fat tree to understand the type of switch we encounter during the iteration.'''
        
    counter = 0
    paths = {}
    tPod = target[1]
    if source[1]==target[1]:
        paths = map(lambda node: [source,node,target], G.neighbors(source))
    else:
        for aggS in G.neighbors(source):
            for core in G.neighbors(aggS):
                #raw_input(core)
                if core[0]=="c":
                    for aggT in G.neighbors(core):
                        #raw_input(aggT)
                        if aggT[0:2]=="a"+tPod:
                            paths[counter]=[source, aggS, core ,aggT, target]  
                            counter +=1
    return paths
        
            
            
          

    
    
def main():  
    user = int(raw_input("\n\nHow many ports per swtich do you want? Please, just even numbers: "))
    G = generateFatTree(user)
    print "Those are the Edge Switches:"
    print sorted(filter(None, map(lambda node: node[0] if node[1]["type"] == "edge" else None,G.nodes(data=True))))
    print "Which path would you like to know?\n"
    again = 1
    while again == 1:
        source = raw_input("Insert source node: ")
        target = raw_input("Insert destination node: ")  
        print "Those are the shortest paths between: " + str((source, target))
        paths = allShortestPaths(G, user, source, target)
        print paths
        print "Those are the disjoint shortest paths between: " + str((source, target))
        dPaths = disjointPaths(G,user,source, target)
        print dPaths 
        #Uncomment to use smart shortest paths
        #print [path for path in smart_all_shortest_paths(G, source, target)]
        again = raw_input("Do you want to continue?(0: NO, 1: YES)")
    nx.draw(G, with_labels=True)
    pylab.savefig(str(user)+"-FatTree")
    plt.show()
    
#if __name__== "__main__":
 #   main() 
    
    

        
    
    
