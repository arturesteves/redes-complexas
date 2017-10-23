import networkx as nx
import sys
import operator

G = nx.read_gml('power.gml', label='id')
n = 4941
if len(sys.argv) > 2:
	n = sys.argv[1]

#For highest degree_centrality
metric_dic = nx.degree_centrality(G)

#For highest betweenes_centrality
#metric_dic = nx.betweenness_centrality(G)

## first sort by the metric in decending order
## than remove one by one n times and for each time compute the
## connected components

nc1 = nx.number_connected_components(G)
print "Number of CC at start = %d" % (nc1)
sorted_nodes = sorted(metric_dic.items(), key=operator.itemgetter(1), reverse=True)

'''
#printing the n top nodes
for i in range(0, n):
	print  sorted_nodes[i]
'''

for i in range(0, n):
	G.remove_node(sorted_nodes[i][0])
	nc2 = nx.number_connected_components(G)
	print "Number of CC at iteration %d = %d" % (i, nc1)




