import networkx as nx
import pickle
import time


def seconds_to_time(time):
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    return "%ddays:%dhours:%dminutes:%dseconds" % (day, hour, minutes, seconds)


start = time.time()


# compute the number of shortest paths that pass through each node. Returns dict
def num_spaths(graph):
    start = time.time()
    n_spaths = dict.fromkeys(graph, 0.0)
    spaths = dict(nx.all_pairs_shortest_path(graph))

    for source in spaths:
        for path in spaths[source].items():
            for node in path[1][1:]:  # ignore first element (source == node)
                n_spaths[node] += 1  # this path passes through `node`

    end = time.time()
    elapsed_time = end - start
    print("It took " + seconds_to_time(
        elapsed_time) + " to compute the number of shortest paths that pass through each node.")
    return n_spaths, spaths


n = 1000  # number of nodes
m = 2  # number of edges for the preferential attachment
graph = nx.barabasi_albert_graph(n, m)  # make a random scale-free graph using barabasi_albert model
nx.write_gpickle(graph, './graph_scalefree_1000.p')

end = time.time()
elapsed_time = end - start
print("It took " + seconds_to_time(elapsed_time) + " to generate the SF graph.")
