import networkx as nx
from collections import OrderedDict
from operator import itemgetter


# GLOBAL VARIABLE
SHORTEST_PATHS_LIST =[]

# record the nodes that you know have been used remote(u,v)  on (add u and v ).
REMOTED_NODES = []

# Contains all the nodes that the majority of votes returned false when scout was used on that node.
# tuple list (student_number, incorrect_votes)
MAJORITY_FALSE = []


def solve(client):
    client.end()
    client.start()

    # call this to populate MAJORITY_FALSE LIST
    students_tuple(client.k)

    # shortest paths dict {node: path from node to H}
    shortest_paths = Djisktras(client.G, client.h)
    reverseListsInShortestPaths(shortest_paths, client.h)  # necessary

    shortest_paths_lengths = Djisktras_length(client.G, client.h)
    shortest_paths_lengths.pop(client.h)  # Gets rid of home node in list

    # ordered dictionary containing paths from largest to smallest of tuples (node, length from H)
    ordered_shortest_paths_lengths = OrderedDict(sorted(shortest_paths_lengths.items(), key=itemgetter(1), reverse=True))


    print(shortest_paths)
    print("")
    print(ordered_shortest_paths_lengths)
    client.end()


# GIVEN A GRAPH G, FIND SHORTEST PATH FROM Home TO EACH vertex
# INPUT IS A NETWORKX GRAPH OBJECT I.E. CLIENT.G AND THE HOME VERTEX
def Djisktras(G, H):
    return nx.single_source_dijkstra_path(G, H)


# gives length of each shortest path (Useful when sorting length edges)
def Djisktras_length(G, H):
    return nx.single_source_dijkstra_path_length(G, H)


def students_tuple(students):
    for i in range(students):
        MAJORITY_FALSE.append((i+1, 1))


def edgeLookup(edgesDict):
    edgesDict


def reverseListsInShortestPaths(d, H):
    for i in d.keys():
        d[i] = list(reversed(d[i]))
    d.pop(H)



