import networkx as nx

graph_name = "scalefree_1000/graph_scalefree_1000"
graph = nx.read_gpickle("./" + graph_name + ".p")

print(nx.info(graph))