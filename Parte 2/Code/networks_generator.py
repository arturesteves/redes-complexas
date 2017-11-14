import networkx as nx
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


def generate_scalefree_network(num_nodes, edges):
    start = time.time()
    graph = nx.barabasi_albert_graph(num_nodes, edges)
    end = time.time()
    nx.write_gpickle(graph, "./networks/graph_scalefree_" + str(num_nodes) + "N_" + str(edges) + "AVD.gpickle")
    print("It took " + seconds_to_time(end - start) + " to generate the homogeneous graph.")


def generate_homogeneous_network(num_nodes, degree):
    start = time.time()
    graph = nx.random_regular_graph(degree, num_nodes)
    end = time.time()
    nx.write_gpickle(graph, "./networks/graph_homogeneous_" + str(num_nodes) + "N_" + str(degree) + "D.gpickle")
    print("It took " + seconds_to_time(end - start) + " to generate the homogeneous graph.")


if __name__ == "__main__":
    print("***** Init networks generation *****")
    # generate scale free network with N = 1000, number of edges to attach from a new node to existing nodes = 2
    generate_scalefree_network(1000, 2)

    # generate homogeneous network with N = 1000, network degree = 3
    generate_homogeneous_network(1000, 3)

    print("***** End networks generation *****")
