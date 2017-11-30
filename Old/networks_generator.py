import networkx as nx
import time
#from random import randint
from random import choice


def seconds_to_time(time):
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    return "%ddays:%dhours:%dminutes:%dseconds" % (day, hour, minutes, seconds)


# estas funcoes tambem podiam retornar o graph


def generate_scalefree_network(num_nodes, edges):
    start = time.time()
    graph = nx.barabasi_albert_graph(num_nodes, edges)
    end = time.time()
    # write file
    nx.write_gpickle(graph, "./networks/scalefree_" + str(num_nodes) + "N_" + str(edges + 1) + "AVD.gpickle")
    print()
    print("***Graph information***")
    print(nx.info(graph))
    print("It took " + seconds_to_time(end - start) + " to generate the homogeneous graph.")

    return graph


def generate_scalefree_network_2(num_nodes, edges):
    start = time.time()
    scale_free_graphs = []
    scale_free_graphs_labels = ()  # tuple containing the prefix name of each node of the graphs
    subnetworks = 10
    nodes_per_network = num_nodes / subnetworks
    # create several scale free networks
    for i in range(0, subnetworks):
        scale_free_graphs.append(nx.barabasi_albert_graph(nodes_per_network, edges))
        scale_free_graphs_labels += (chr(i + 65) + "-"),

    graph = nx.Graph()  # crete empty graph
    graph.add_node(1)  # add node 1

    scale_free_graphs.append(graph)
    # add all the scale free networks to the empty graph created
    graph = nx.union_all(scale_free_graphs, rename=scale_free_graphs_labels)

    # append the '1' node to
    for i in range(0, len(scale_free_graphs)-1):
        random_node = choice(list(scale_free_graphs[i].nodes()))
        graph.add_edge(1, (scale_free_graphs_labels[i] + str(random_node)))

    end = time.time()
    # write to file
    nx.write_gpickle(graph, "./networks/scalefree2_" + str(num_nodes) + "N_" + str(edges + 1) + "AVD.gpickle")
    # print graph information
    print()
    print("***Graph information***")
    print(nx.info(graph))
    print("It took " + seconds_to_time(end - start) + " to generate the scalefree graph where the node with "
                                                      "the highest load doesn't have the highest degree.")

    return graph


def generate_homogeneous_network(num_nodes, degree):
    start = time.time()
    graph = nx.random_regular_graph(degree, num_nodes)
    end = time.time()
    nx.write_gpickle(graph, "./networks/homogeneous_" + str(num_nodes) + "N_" + str(degree) + "D.gpickle")
    print()
    print("***Graph information***")
    print(nx.info(graph))
    print("It took " + seconds_to_time(end - start) + " to generate the homogeneous graph.")


if __name__ == "__main__":
    print("***** Init networks generation *****")
    # generate scale free network with N = 1000, number of edges to attach from a new node to existing nodes = 1,
    # giving an average degree of approximately 2
    #generate_scalefree_network(1000, 1)

    # generate homogeneous network with N = 1000, network degree = 3
    #generate_homogeneous_network(1000, 3)

    generate_scalefree_network_2(1000, 1)
    print()
    print("***** End networks generation *****")
