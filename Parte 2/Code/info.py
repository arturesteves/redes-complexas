import networkx as nx
import sys

try:
	graph = nx.read_gexf(sys.argv[1])
	print(nx.info(graph))
except:
	print("Path not found")
