import networkx as nx
import pickle

n = 5000  # number of nodes
m = 2  # number of edges for the preferential attachment
graph = nx.barabasi_albert_graph(n, m)  # make a random scale-free graph using barabasi_albert model
nx.write_gpickle(graph, './graph_scalefree_5000.txt')