import networkx as nx
import pickle
import time

def seconds_to_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)

start = time.time()


n = 2000  # number of nodes
m = 1  # number of edges for the preferential attachment
graph = nx.barabasi_albert_graph(n, m)  # make a random scale-free graph using barabasi_albert model
nx.write_gpickle(graph, './graph_scalefree_'+str(n)+'_'+str(m)+'.p')
print("info: ", nx.info(graph))

end = time.time()
elapsed_time = end - start
print("It took " + seconds_to_time(elapsed_time) + " to generate the SF graph.")