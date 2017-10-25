'''
    This project is based on python 3.6.1


    TODOS:
        Generate metrics:
            Average Degree - x
            Degree Distribution - x
            Average Path Length - x
            Eigenvector Centrality


        Print metrics in file - x
        Print metrics in a file for every iteration - x
        Save the plots for every iteration (save as pdf file, at least for now) - x
        Plot average path length only after the iteration process is completed


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
import sys
import csv


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


# orders the nodes using the metric
def get_ordered_nodes(graph):
    # For highest degree_centrality
    # metric_dic = nx.degree_centrality(G)

    # For highest betweenness_centrality
    metric_dic = nx.betweenness_centrality(graph)
    sorted_nodes = sorted(metric_dic.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_nodes


# todo: fazer com que esta funcao aceite a metrica e a ordem com que os nos devem ser removidos
# assim da para fazer uma comparacao entre metricas
# plot graph after iterations
def print_iterations(network_name, graph, iterations, jump, strategy=None):
    print("Init print iterations...")
    # todo: receber a estrategia de attack, aqui é pela betwenneess e a outra por agora sera a random; acrescentar a random aqui
    sorted_nodes = get_ordered_nodes(graph)
    print("Graph sorted by betweenness")
    print("Starting iterations...")
    figure = plt.figure()
    figure.canvas.set_window_title(network_name)
    for i in range(0, iterations):
        node_to_remove = sorted_nodes[i][0]
        print("Removing node: %s", node_to_remove)
        # graph.remove_node(node_to_remove)
        graph.remove_node(node_to_remove)
        # to skip ploting all iterations, zero and multiples of jump
        if i % jump == 0:
            nx.draw(graph, pos=nx.spring_layout(graph), node_size=5, node_color='orange')

            #  calculate metrics
            nodes = len(nx.nodes(graph))
            edges = len(nx.edges(graph))
            average_degree = compute_average_degree(graph)
            number_nodes_removed = jump
            removed_nodes_percentage = ((nodes - jump) * 100) / nodes
            connected_components = nx.connected_components(graph)
            number_connected_components = nx.number_connected_components(graph)
            max_connected_component_size = max(connected_components,
                                               key=len)  # todo: alterar isto, para retornar o número e nao uma lista gigante

            # fetch the greater connected component, because of the apl
            larger_connected_component = max(nx.connected_component_subgraphs(graph), key=len)
            average_path_length = nx.average_shortest_path_length(larger_connected_component)

            # about average path length: try floyd_warshall and astar_path (explicar relatorio se valer a pena)

            nodes_centrality = nx.eigenvector_centrality(graph)

            # EigenVector Centrality
            # ver mas métricas que estão no pdf

            #  end metrics
            write_iteration_metrics(num_nodes=nodes, num_edges=edges, average_degree=average_degree,
                                    number_nodes_removed=number_nodes_removed,
                                    removed_nodes_percentage=removed_nodes_percentage,
                                    number_connected_components=number_connected_components,
                                    max_connected_component_size=max_connected_component_size,
                                    average_path_length=average_path_length,
                                    network_name=network_name, iteration=i)

            print("Number of the iteration: " + str(i))
            plt.title("Network: " + network_name + " - Iteration " + str(i))
            plt.suptitle("Network: " + network_name + " - Iteration " + str(i))
            # plt.annotate('Connected Components: ' + str(number_connected_components), xy=(0.1, 0.1), xytext=(0.112, 0.15))
            plt.draw()
            plt.savefig("networks/output/Network " + network_name + " - Iteration " + str(i) + ".pdf")
            # plt.show()
            plt.close()
            plt.gcf().clear()  # forget old plot

    pass
    # here plot the average path length plot, outside the for loop


def compute_average_degree(graph):
    # graph.edges returns a list of tuples with the node and a neighbor
    return (2 * len(graph.edges)) / len(graph.nodes)


def generic_plot(**kwargs):
    plt.figure()
    plt.grid(kwargs.pop("grid", False))
    plt.plot(kwargs.pop("x_axis", []), kwargs.pop("y_axis", []), kwargs.pop("plot_style", "b-"))
    plt.yscale(kwargs.pop("y_scale", "linear"))
    plt.xscale(kwargs.pop("x_scale", "linear"))
    plt.xlabel(kwargs.pop("x_label", ""))
    plt.ylabel(kwargs.pop("y_label", ""))
    plt.title(kwargs.pop("title", ""))
    plt.savefig("networks/output/" + kwargs.pop("file_name") + ".pdf")
    plt.close()
    plt.gcf().clear()  # forget old plot


# plot number of nodes x average length of paths
# faz sentido quando se estiverem a retirar os nós!
# nodes: number of nodes; average_path_length: list of values of the paths according with
# the nodes number, this list should be order from when there is fewer nodes to the a full node scene
# plot example: https://www.researchgate.net/figure/270222207_fig13_Comparisons-of-average-length-for-all-paths
def plot_average_path_length_vs_nodes(graph, nodes, average_path_length, ):
    # todo: call with proper parameters
    generic_plot()
    pass


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
    with open("networks/output/" + kwargs.pop("network_name") + "_attack_metrics.txt", 'a+') as file:
        file.write("Iteration number: {0}\n".format(kwargs.pop("iteration")))
        file.write("Number of nodes: {0}\n".format(kwargs.pop("num_nodes")))
        file.write("Number of edges: {0}\n".format(kwargs.pop("num_edges")))
        file.write("Average degree: {0}\n".format(kwargs.pop("average_degree")))
        file.write("Number of nodes removed: {0}\n".format(kwargs.pop("number_nodes_removed")))
        file.write("Percentage of nodes removed: {0}\n".format(kwargs.pop("removed_nodes_percentage")))
        file.write("Number of connected components: {0}\n".format(kwargs.pop("number_connected_components")))
        file.write("Size of the biggest connected component: {0}\n".format(kwargs.pop("max_connected_component_size")))
        file.write("Average path length: {0}\n".format(kwargs.pop("average_path_length")))
        file.write("--------------------------------------------------\n")


if __name__ == "__main__":
    # runs scripts
    print("Network analysis")
    biological_network = 'diseasome'
    power_network = 'power'
    iterations = 101
    graph = load_graph(network_name=biological_network)
    '''
     run 30 iterations on graph G to remove critical nodes
     based on the metric betweenness centrality and plot the
     graph every 5 iterations
    '''
    print_iterations(biological_network, graph, iterations, 20)
    graph = load_graph(network_name=power_network)
    print_iterations(power_network, graph, iterations, 20)

    # compute_average_degree(graph)
    # degree_distribution(graph, network_name)
