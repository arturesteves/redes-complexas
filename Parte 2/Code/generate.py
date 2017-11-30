import networkx as nx
import time
import sys
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
    nx.write_gexf(graph, "./networks/" + name + ".gexf")

def generate_homogeneous_network(num_nodes, degree, filename=""):
    start = time.time()
    graph = nx.random_regular_graph(degree, num_nodes)
    end = time.time()
    # write to file
    if filename != "":
        write_network_to_file(graph, filename)
    # print graph information
    end_generation_info(graph, end - start, "homogeneous")
    return graph


def generate_attempt1(num_nodes, edges, filename=""):
    start = time.time()
    graph = nx.barabasi_albert_graph(num_nodes, edges)
    end = time.time()
    if filename != "":
        # write to file
        write_network_to_file(graph, filename)
    # print graph information
    end_generation_info(graph, end - start, "scale-free")
    return graph

def generate_attempt2(num_nodes, edges=2, filename=""):
    start = time.time()
    scale_free_graphs = []
    scale_free_graphs_labels = ()  # tuple containing the prefix name of each node of the graphs
    subnetworks = 10
    nodes_per_network = num_nodes / subnetworks
    # create several scale free networks
    for i in range(0, subnetworks):
        scale_free_graphs.append(nx.barabasi_albert_graph(nodes_per_network, edges))
        #tempGraph = nx.scale_free_graph(nodes_per_network, alpha=0.1, beta=0.6, gamma=0.3, delta_in=0.4, delta_out=0, create_using=None, seed=None)
        #tempGraph = tempGraph.to_undirected()
        #scale_free_graphs.append(tempGraph)
        scale_free_graphs_labels += (chr(i + 65) + "-"),  # node labeling

    graph = nx.Graph()  # crete empty graph
    graph.add_node(1)  # add node 1

    scale_free_graphs.append(graph)
    # add all the scale free networks to the empty graph created
    graph = nx.union_all(scale_free_graphs, rename=scale_free_graphs_labels)

    # connect the node '1' to a node on every other scale free network
    for i in range(0, len(scale_free_graphs)-1):
        random_node = choice(list(scale_free_graphs[i].nodes()))
        graph.add_edge(1, (scale_free_graphs_labels[i] + str(random_node)))

    end = time.time()
    if filename != "":
        # write to file
        write_network_to_file(graph, filename)
    # print graph information
    end_generation_info(graph, end - start, "scale-free", "Note: the node with the highest load doesn't have the "
                                                          "highest degree.")
    return graph


def generate_attempt3(num_nodes, edges, filename=""):
    start = time.time()
    scale_free_graphs = []
    scale_free_graphs_labels = ()  # tuple containing the prefix name of each node of the graphs
    subnetworks = 10
    nodes_per_network = num_nodes / subnetworks
    # create several scale free networks
    for i in range(0, subnetworks):
        scale_free_graphs.append(nx.barabasi_albert_graph(nodes_per_network, edges))
        # tempGraph = nx.scale_free_graph(nodes_per_network, alpha=0.1, beta=0.6, gamma=0.3, delta_in=0.4, delta_out=0, create_using=None, seed=None)
        # tempGraph = tempGraph.to_undirected()
        # scale_free_graphs.append(tempGraph)
        scale_free_graphs_labels += (chr(i + 65) + "-"),  # node labeling

    # crete another scalefree network which random nodes inside will connect to the other networks
    graph = nx.barabasi_albert_graph(nodes_per_network, edges)

    scale_free_graphs.append(graph)
    # add all the scale free networks to the empty graph created
    graph = nx.union_all(scale_free_graphs, rename=scale_free_graphs_labels)

    random_nodes_central_network = []
    # connect the node '1' to a node on every other scale free network
    for i in range(0, len(scale_free_graphs) - 1):
        random_node = choice(list(scale_free_graphs[i].nodes()))  # choose random node from a scale free network
        random_node_central_network = choice(list(graph.nodes()))
        random_nodes_central_network.append(random_node_central_network)
        graph.add_edge(random_node_central_network, (scale_free_graphs_labels[i] + str(random_node)))

    # choose a random node in the central network
    nodes = list(graph.nodes())
    # prevent the central node from having a connection directly to the others surrounded networks
    nodes_allowed = [x for x in nodes if x not in random_nodes_central_network]
    central_random_node = choice(list(nodes_allowed))

    for node in random_nodes_central_network:
        graph.add_edge(central_random_node, node)

    for node in random_nodes_central_network:
        for n in random_nodes_central_network:
            if node != n:
                graph.add_edge(node, n)

    end = time.time()
    if filename != "":
        # write to file
        write_network_to_file(graph, filename)
    # print graph information
    end_generation_info(graph, end - start, "scale-free", "Note: the node with the highest load doesn't have the "
                                                          "highest degree.")
    return graph


if __name__ == "__main__":
    print("***** Init network generation *****")

    attempt = sys.argv[1]
    n = int(sys.argv[2])
    edges = int(sys.argv[3])
    degree = int(sys.argv[3])
    

    if attempt == 'attempt1':
        graph = generate_attempt1(n, edges)
        nx.info(graph)
    elif attempt == 'attempt2':
        graph = generate_attempt2(n, edges)
        nx.info(graph)
    elif attempt == 'attempt3':
        graph = generate_attempt3(n, edges)
        nx.info(graph)
    elif attempt == 'homogeneous':
        graph = generate_homogeneous_network(n, degree)
        nx.info(graph)
    else: 
        print("ERROR: Not a valid mode of generation, the only valid modes of generation are:")
        print("  attemp1")
        print("  attemp2")
        print("  attemp3")
        print("  homogeneous")
        print("Example: \n> python generate.py homogeneous 1000 3")

    print("***** End network generation *****")
