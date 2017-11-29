import networkx as nx
import time
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


def end_generation_info(graph, time, graph_type, extra=""):
    print()
    print("***Graph information***")
    print(nx.info(graph))
    print("It took " + seconds_to_time(time) + " to generate the " + graph_type + " network. " + extra)
    print()


def write_network_to_file(graph, name):
    nx.write_gpickle(graph, "./networks/" + name + ".gpickle")


def generate_scalefree_network(num_nodes, edges):
    start = time.time()
    graph = nx.scale_free_graph(num_nodes, alpha=0.1, beta=0.6, gamma=0.3, delta_in=0.4, delta_out=0, create_using=None, seed=None)
    graph = graph.to_undirected()
    end = time.time()
    # write to file
    write_network_to_file(graph, "scalefree_" + str(num_nodes) + "N_" + str(edges) + "AVD")
    # print graph information
    end_generation_info(graph, end - start, "scale-free")
    return graph


def generate_homogeneous_network(num_nodes, degree):
    start = time.time()
    graph = nx.random_regular_graph(degree, num_nodes)
    end = time.time()
    # write to file
    write_network_to_file(graph, "homogeneous_" + str(num_nodes) + "N_" + str(degree) + "AVD")
    # print graph information
    end_generation_info(graph, end - start, "homogeneous")
    return graph


def generate_scalefree_network_2(num_nodes, edges=99999):
    start = time.time()
    scale_free_graphs = []
    scale_free_graphs_labels = ()  # tuple containing the prefix name of each node of the graphs
    subnetworks = 10
    nodes_per_network = num_nodes / subnetworks
    # create several scale free networks
    for i in range(0, subnetworks):
        #scale_free_graphs.append(nx.barabasi_albert_graph(nodes_per_network, edges - 1))
        tempGraph = nx.scale_free_graph(nodes_per_network, alpha=0.1, beta=0.6, gamma=0.3, delta_in=0.4, delta_out=0, create_using=None, seed=None)
        tempGraph = tempGraph.to_undirected()
        scale_free_graphs.append(tempGraph)
        scale_free_graphs_labels += (chr(i + 65) + "-"),  # node labeling

    graph = nx.MultiGraph()  # crete empty graph
    graph.add_node(1)  # add node 1

    scale_free_graphs.append(graph)
    # add all the scale free networks to the empty graph created
    graph = nx.union_all(scale_free_graphs, rename=scale_free_graphs_labels)

    # connect the node '1' to a node on every other scale free network
    for i in range(0, len(scale_free_graphs)-1):
        random_node = choice(list(scale_free_graphs[i].nodes()))
        graph.add_edge(1, (scale_free_graphs_labels[i] + str(random_node)))

    end = time.time()
    # write to file
    write_network_to_file(graph, "scalefree2_" + str(num_nodes + 1) + "N_" + str(edges) + "AVD")
    # print graph information
    end_generation_info(graph, end - start, "scale-free", "Note: the node with the highest load doesn't have the "
                                                          "highest degree.")
    return graph


def load_usa_network():
    file = open("./western_usa_power_grid_network/opsahl_powergrid.edgelist", 'rb')
    graph = nx.read_edgelist(file)
    return graph


def load_default_networks():
    graph_1 = generate_scalefree_network(1000, 2)
    graph_2 = generate_homogeneous_network(1000, 3)
    graph_3 = generate_scalefree_network_2(1000, 2)


if __name__ == "__main__":
    print("***** Init networks generation *****")

    # generate scale free network with N = 1000, number of edges to attach from a new node to existing nodes = 1,
    # giving an average degree of approximately 2
    # The degree with the highest degree is the on with the highest load (load is given by the numbers of shortest paths
    # that pass trough the node)
    graph_1 = generate_scalefree_network(1000, 2)

    # generate homogeneous network with N = 1000, average node degree = 3
    graph_2 = generate_homogeneous_network(1000, 3)

    # generate scale free network with N = 1000, average node = 2;
    # The node with the highest degree doesn't have the highest load
    graph_3 = generate_scalefree_network_2(1000, 2)
    nx.write_edgelist(graph_3, "./networks/st.edgelist")

    # load usa western power grid
    graph_4 = load_usa_network()
    print(nx.info(graph_4))
    print("***** End networks generation *****")