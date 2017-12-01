'''
    This project is based on python 3.6.1

    Docs support:
        https://www.cl.cam.ac.uk/teaching/1314/L109/tutorial.pdf
        https://www.cl.cam.ac.uk/~cm542/teaching/2010/stna-pdfs/stna-lecture8.pdf
        http://www.math.pitt.edu/~lewicka/Semester_DiscrNetw_14/MNlecture22.pdf
        http://samoa.santafe.edu/media/cms_page_media/420/CSSS2012_report__Alex_Marco_Ian_Shin_4.pdf
        http://barabasi.com/f/687.pdf
        http://barabasi.com/f/619.pdf
        Capítulo 6: https://www.dropbox.com/s/q2zis23qa4jv2vv/BarratBarthelemyVespignani-DynamicalProcessesOnComplexNetworks.pdf?dl=0
'''
import matplotlib.pyplot as plt
import networkx as nx
import operator
import csv
import imageio
import random


# import numpy as np

# load a graph using the name of the network in the current folder
def load_graph(network_name="diseasome"):
    G = nx.Graph()
    f = True
    with open('networks/' + 'nodes_' + network_name + '.csv', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if (f == True):
                f = False
                continue
            G.add_node(row[0])

    f = True
    with open('networks/' + 'edges_' + network_name + '.csv', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if (f == True):
                f = False
                continue
            G.add_edge(row[0], row[1])

    return G


# orders nodes using one metric
def sort_nodes_by_metric(graph, metric):
    nodes = None
    sorted_nodes = []

    # switch by metric
    if metric == "degree_centrality":
        nodes = nx.degree_centrality(graph)
        sorted_nodes = sorted(nodes.items(), key=operator.itemgetter(1), reverse=True)
    elif metric == "betweenness_centrality":
        nodes = nx.betweenness_centrality(graph)
        sorted_nodes = sorted(nodes.items(), key=operator.itemgetter(1), reverse=True)
    elif metric == "random":
        nodes = nx.betweenness_centrality(graph)
        sorted_nodes_aux = nodes
        values = list(sorted_nodes_aux.values())
        random.shuffle(values)
        sorted_nodes_aux = dict(zip(sorted_nodes_aux.keys(), values))

        for key, value in sorted_nodes_aux.items():
            sorted_nodes.append((key, value))

    return sorted_nodes


# plot graph after iterations
def attack_network(network_name, graph, iterations, jump, metric="degree_centrality"):
    print("Attack " + network + " by " + metric + "...")
    # nodes sorted by highest betweenness centrality
    sorted_nodes = sort_nodes_by_metric(graph, metric)
    print("Graph sorted by " + metric)
    original_number_nodes = len(sorted_nodes)
    n, e, ad, nnr, rnp, ncc, lcc, apl, aplacc, dlcc, dc, bc = calculate_metrics(graph, 0, original_number_nodes)

    # plot original graph
    plot_graph(graph=graph, title="Network: " + network_name + " Original",
               file_name=network_name + " - " + metric + " - Original", extension="png",
               x_axis=original_number_nodes, metric=metric, dc=dc, bc=bc, r=sorted_nodes)

    #  write metrics
    write_iteration_metrics(num_nodes=n, num_edges=e, average_degree=ad,
                            number_nodes_removed=nnr,
                            removed_nodes_percentage=rnp,
                            number_connected_components=ncc,
                            max_connected_component_size=lcc,
                            average_path_length=apl,
                            average_path_length_all_cc=aplacc,
                            network_name=network_name,
                            diameter_largest_connected_component=dlcc,
                            degree_centrality=dc,
                            betweenness_centrality=bc,
                            iteration=0)

    for i in range(1, iterations):
        node_to_remove = sorted_nodes[i][0]
        print("Removing node: %s", node_to_remove)
        graph.remove_node(node_to_remove)

        # to skip ploting all iterations
        if i % jump == 0:
            print("save iteration: " + str(i))
            #  calculate metrics
            n, e, ad, nnr, rnp, ncc, lcc, apl, aplacc, dlcc, dc, bc = calculate_metrics(graph, i, original_number_nodes)
            #  write metrics
            plot_graph(graph=graph, title="Network: " + network_name + " - Iteration " + str(i),
                       file_name=network_name + " - " + metric + " - Iteration " + str(i), extension="png",
                       x_axis=n, metric=metric, dc=dc, bc=bc, r=sorted_nodes)

            write_iteration_metrics(num_nodes=n, num_edges=e, average_degree=ad,
                                    number_nodes_removed=nnr,
                                    removed_nodes_percentage=rnp,
                                    number_connected_components=ncc,
                                    max_connected_component_size=lcc,
                                    average_path_length=apl,
                                    average_path_length_all_cc=aplacc,
                                    network_name=network_name,
                                    diameter_largest_connected_component=dlcc,
                                    degree_centrality=dc,
                                    betweenness_centrality=bc,
                                    iteration=i)

            print("Number of the iteration: " + str(i))

    print("End of attack")


def calculate_metrics(graph, iteration, original_number_nodes):
    print("calculate metrics...")
    nodes = len(nx.nodes(graph))
    edges = len(nx.edges(graph))
    average_degree = compute_average_degree(graph)
    number_nodes_removed = iteration
    removed_nodes_percentage = (number_nodes_removed * 100) / original_number_nodes
    connected_components = nx.connected_components(graph)
    number_connected_components = nx.number_connected_components(graph)
    max_connected_component_size = max(connected_components,
                                       key=len)

    # fetch the greater connected component, because of the apl
    larger_connected_subgraph = max(nx.connected_component_subgraphs(graph), key=len)
    larget_connected_graph_nodes = len(larger_connected_subgraph.nodes)
    larger_connected_component = max(larger_connected_subgraph)
    average_path_length_largest_connected_component = nx.average_shortest_path_length(larger_connected_subgraph)
    diameter_largest_connected_component = nx.diameter(larger_connected_subgraph)
    # average_path_length = nx.average_shortest_path_length(graph)

    connected_components_graphs = nx.connected_component_subgraphs(graph)
    average_path_length_all_connected_components = []
    for component in connected_components_graphs:
        average_path_length_all_connected_components.append(nx.average_shortest_path_length(component))

    # eigenvector_centrality = nx.eigenvector_centrality(graph)
    degree_centrality = nx.degree_centrality(graph)
    betweenness_centrality = nx.betweenness_centrality(graph)

    print("calculate metrics...")
    return (nodes, edges, average_degree, number_nodes_removed, removed_nodes_percentage,
            number_connected_components,
            larger_connected_component, average_path_length_largest_connected_component,
            average_path_length_all_connected_components, diameter_largest_connected_component,
            degree_centrality, betweenness_centrality)


def compute_average_degree(graph):
    # graph.edges returns a list of tuples with the node and a neighbor
    return (2 * len(graph.edges)) / len(graph.nodes)


def plot_graph(**kwargs):
    print("Init plotting...")
    graph = kwargs.pop("graph")
    if graph is not None:
        nodes_sorted = None
        factor = None
        metric = kwargs.pop("metric")
        if metric == "degree_centrality":
            factor = 1000
            nodes_sorted = kwargs.pop("dc")
        elif metric == "betweenness_centrality":
            factor = 500
            nodes_sorted = kwargs.pop("bc")
        elif metric == "random":
            factor = 500
            nodes_sorted = dict(kwargs.pop("r"))

        plt.figure()
        nx.draw(graph, pos=nx.spring_layout(graph), node_size=[v * factor for v in nodes_sorted.values()],
                node_color='orange')
        plt.grid(kwargs.pop("grid", False))
        # plt.plot(kwargs.pop("x_axis", []), kwargs.pop("y_axis", []), kwargs.pop("plot_style", "b-"))
        plt.yscale(kwargs.pop("y_scale", "linear"))
        plt.xscale(kwargs.pop("x_scale", "linear"))
        plt.xlabel(kwargs.pop("x_label", ""))
        plt.ylabel(kwargs.pop("y_label", ""))
        plt.title(kwargs.pop("title", ""))
        plt.savefig("networks/output/" + kwargs.pop("file_name") + "." + kwargs.pop("extension", "png"))
        # plt.show()
        plt.close()
        plt.gcf().clear()  # forget old plot

    print("End plotting...")


# currently plotting
def degree_distribution(graph, network_name):
    node_degree = graph.degree(graph.nbunch_iter())  # dictionary node: degree
    nodes = graph.nodes
    degrees = [int(x[1]) for x in node_degree]  # remove just the degrees
    print(nodes)
    plt.figure()
    plt.grid(True)
    plt.plot(degrees, nodes, 'ro-')
    plt.yscale('log')
    plt.legend(['Degree'])
    plt.xlabel('Degree')
    plt.ylabel('Number of nodes')
    plt.title('Degree Distribution of ' + network_name + " network")
    plt.savefig("networks/output/" + network_name + "_degree_distribution.pdf")
    plt.show()
    plt.close()
    plt.gcf().clear()  # forget old plot


def write_iteration_metrics(**kwargs):
    # graph, network_name, iteration):
    print("Writing to file...")
    with open("networks/output/" + kwargs.pop("network_name") + " - " + metric + " - attack.txt", 'a+') as file:
        file.write("Iteration number: {0}\n".format(kwargs.pop("iteration")))
        file.write("Number of nodes: {0}\n".format(kwargs.pop("num_nodes")))
        file.write("Number of edges: {0}\n".format(kwargs.pop("num_edges")))
        file.write("Average degree: {0}\n".format(kwargs.pop("average_degree")))
        file.write("Number of nodes removed: {0}\n".format(kwargs.pop("number_nodes_removed")))
        file.write("Percentage of nodes removed: {0}%\n".format(kwargs.pop("removed_nodes_percentage")))
        file.write("Number of connected components: {0}\n".format(kwargs.pop("number_connected_components")))
        file.write(
            "Size of the biggest connected component: {0} nodes\n".format(kwargs.pop("max_connected_component_size")))
        file.write(
            "Average path length of largest connected component: {0}\n".format(kwargs.pop("average_path_length")))
        file.write(
            "Average path length of all connected components: {0}\n".format(kwargs.pop("average_path_length_all_cc")))
        file.write(
            "Diameter largest connected component: {0}\n".format(kwargs.pop("diameter_largest_connected_component")))
        # file.write("Eigenvector centrality: {0}\n".format(kwargs.pop("eigenvector_centrality")))
        file.write("Degree centrality: {0}\n".format(kwargs.pop("degree_centrality")))
        file.write("Betweenness centrality: {0}\n".format(kwargs.pop("betweenness_centrality")))
        file.write("--------------------------------------------------\n")

    print("End writing to file.")


def generate_gif(network, iterations, jump, metric):
    base = "networks/output/" + network
    filenames = [base + " - " + metric + " - Original.png"]
    for i in range(1, iterations):
        if i % jump == 0:
            filenames.append(base + " - " + metric + " - Iteration " + str(i) + ".png")

    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))

    imageio.mimsave(base + " - " + metric + " - attack.gif", images, duration=0.5)
    print("\n " + base + " - " + metric + " - attack.gif, has been generated\n\n")


if __name__ == "__main__":
    # running this script will take several minutes
    print("Network analysis")
    iterations = 101
    jump = 20

    network = "diseasome"
    metric = "degree_centrality"
    graph = load_graph(network_name=network)
    attack_network(network, graph, iterations, jump, metric)
    generate_gif(network, iterations, jump, metric)

    metric = "betweenness_centrality"
    graph = load_graph(network_name=network)
    attack_network(network, graph, iterations, jump, metric)
    generate_gif(network, iterations, jump, metric)

    metric = "random"
    graph = load_graph(network_name=network)
    attack_network(network, graph, iterations, jump, metric)
    generate_gif(network, iterations, jump, metric)

    network = "power"
    metric = "degree_centrality"
    graph = load_graph(network_name=network)
    attack_network(network, graph, iterations, jump, metric)
    generate_gif(network, iterations, jump, metric)

    metric = "betweenness_centrality"
    graph = load_graph(network_name=network)
    attack_network(network, graph, iterations, jump, metric)
    generate_gif(network, iterations, jump, metric)

    metric = "random"
    graph = load_graph(network_name=network)
    attack_network(network, graph, iterations, jump, metric)
    generate_gif(network, iterations, jump, metric)
