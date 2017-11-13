
import matplotlib.pyplot as plt
import networkx as nx

#tests

G = nx.path_graph(5)
nx.draw(G)
#plt.savefig("simple_path.png")  # save as png
plt.show()  # display
spaths = dict(nx.all_pairs_shortest_path(G))
n_spaths = dict.fromkeys(G, 0.0)
nodes_spaths_pass_through_nodes = {node: set() for node in G.nodes}  # each node has a list of nodes that

print("spaths: ", spaths)
print("")
for source in spaths:
    print("source: ", source)
    for path in spaths[source].items():
        print("    path: ", path)
        for node in path[1][1:]:  # ignore first element (source == node)
            print("        node: ", node)
            n_spaths[node] += 1  # this path passes through `node`
            nodes_spaths_pass_through_nodes[source].add(node)

list_nodes = [0, 1, 2, 3, 4]
__spaths = {}  # empty dictionary
for n in list_nodes:
    __spaths[n] = nx.single_source_shortest_path(G, n)

print("__spath: ", __spaths)

print("n_spath: ", n_spaths)
print("nodes_spaths_pass_through_nodes: ", nodes_spaths_pass_through_nodes)
            #nodes_spaths_pass_through_nodes


#print(spaths)
#print(spaths[0].items())  # path
#path = spaths[0].items()
#node = path[1][1:]
#print(node)


#for source in spaths:
#    for path in spaths[source].items():
#        for node in path[1][1:]:  # ignore first element (source == node)
#            n_spaths[node] += 1  # this path passes through `node`
#            nodes_spaths_pass_through_nodes


d1={1:2,3:4}
d2={5:6,7:9,1:50}
#d2={}
d3={**d1, **d2}

#d3={10:8,13:22}
#d4 = dict(d1, **d2)
#d4.update(d3)

print(d1)
print(d2)
print(d3)
#print(d4)

#

