import networkx as nx
from random import randint
import pickle
import time
import copy


def seconds_to_time(time):
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    return "%ddays:%dhours:%dminutes:%dseconds" % (day, hour, minutes, seconds)


# compute the number of shortest paths that pass through each node. Returns dict
def num_spaths(graph):
    start = time.time()
    n_spaths = dict.fromkeys(graph, 0.0)
    spaths = dict(nx.all_pairs_shortest_path(graph))

    for source in spaths:
        for path in spaths[source].items():
            if len(path[1]) == 1:  # self path
                continue
            for node in path[1][1:]:  # ignore first element (source == node)
                n_spaths[node] += 1  # this path passes through `node`

    end = time.time()
    elapsed_time = end - start
    print("It took " + seconds_to_time(
        elapsed_time) + " to compute the number of shortest paths that pass through each node.")
    return n_spaths, spaths


# compute the number of shortest paths that pass through each node.
def num_spaths_update(graph, loads, spaths, removed_nodes):
    # The nodes in the graph were already removed

    print("Nodes removed: ", removed_nodes)
    # remove all the paths whose nodes removed are either the source or the target of the shortest paths
    for rnode in removed_nodes:
        if rnode in list(spaths):
            del spaths[rnode]
        for source in list(spaths):
            if rnode in list(spaths[source]):
                del spaths[source][rnode]

    # remove the entries of the nodes that were removed
    for node in removed_nodes:
        del loads[node]

    number_of_calculations = 0
    for source in list(spaths):
        source_dict = spaths[source]
        for target in list(source_dict):

            path = source_dict[target]
            remove_path = False

            # if any node in the path were removed a flag is raised
            for node in path:
                if node in removed_nodes:
                    remove_path = True
                    break

            if remove_path:
                # decrement the loads from the removed shortest path
                for node in path:
                    if node in loads:
                        loads[node] -= 1

                # recalculate path
                try:
                    number_of_calculations += 1
                    new_path = nx.shortest_path(graph, source=source, target=target)
                    spaths[source][target] = new_path
                    # increment the loads with the new shortest path
                    for node in new_path:
                        loads[node] += 1
                except nx.NetworkXNoPath:
                    pass

    print("Number of shortest paths recalculated", number_of_calculations)


def cascade(graph, initial_loads, spaths, tolerance, node_removed):
    stable = False
    removed_nodes = [node_removed]
    current_load = initial_loads.copy()
    current_spaths = spaths
    while not stable:
        stable = True
        print("Number of nodes removed: ", len(removed_nodes))
        # passing through reference themselves current_load and spaths
        num_spaths_update(graph, current_load, current_spaths, removed_nodes)
        removed_nodes = []
        for node_load in current_load.items():
            node = node_load[0]
            load = node_load[1]
            if load > (1 + tolerance) * initial_loads[node]:
                graph.remove_node(node)
                removed_nodes.append(node)
                stable = False


# removes a random node and cascades
def remove_random(graph, initial_loads, spaths, tolerance):
    nodes = list(graph.nodes())
    index = randint(0, len(nodes) - 1)
    graph.remove_node(nodes[index])
    print("Node Removed: " + str(nodes[index]))
    cascade(graph, initial_loads, spaths, tolerance, nodes[index])


# removes a node by highest degree and cascades
def remove_highest_degree(graph, initial_loads, spaths, tolerance):
    degrees = dict(graph.degree())
    index = max(degrees, key=degrees.get)
    graph.remove_node(index)
    print("Node Removed: " + str(index))
    cascade(graph, initial_loads, spaths, tolerance, index)


# removes a node by highest load and cascades
def remove_highest_load(graph, initial_loads, spaths, tolerance):
    index = max(initial_loads, key=initial_loads.get)
    graph.remove_node(index)
    print("Node Removed" + str(index))
    cascade(graph, initial_loads, spaths, tolerance, index)


# simulates the removal of a node and calculates the cascading effect
def simulate(graph, initial_loads, spaths, tolerance, removal_function):
    # calculate the size of the giant component  before removing
    component_sizes = list(map(lambda sg: nx.number_of_nodes(sg), list(nx.connected_component_subgraphs(graph))))
    N = max(component_sizes) if len(component_sizes) > 0 else 0

    # remove the node and cascade
    removal_function(graph, initial_loads, spaths, tolerance)

    # calculate the size of the giant component  after removing
    component_sizes = list(map(lambda sg: nx.number_of_nodes(sg), list(nx.connected_component_subgraphs(graph))))
    N_prime = max(component_sizes) if len(component_sizes) > 0 else 0

    G = N_prime / N if N != 0 else 0

    print("Tolerance", tolerance)
    print("Global size: ", nx.number_of_nodes(graph))
    print("Giant Component size: ", N_prime)
    print("N: ", N)
    print("N': ", N_prime)
    print("G: ", G)

    #return [tolerance, nx.number_of_nodes(graph), N, N_prime, G]
    return {"tolerance": tolerance, "graph-size": nx.number_of_nodes(graph), "N": N,
            "N_prime": N_prime, "G": G}


def write_simulation_info_to_file(graph_name, strategy, sim_result):
    with open("./data/" + graph_name + "_removed_by_" + strategy, "a") as file:
        for line in sim_result:
            file.write(str(line) + "\n")


# todo: colocar timers entre cada simulacao
def all_simulatons(graph, initial_loads, spaths, tolerances, graph_name):
    # run the simulation for each tolerance value
    simulation_results1 = []
    simulation_results2 = []
    simulation_results3 = []
    start = None
    end = None
    for tolerance in tolerances:
        print()
        print()
        print("**** Simulating with tolerance: " + str(tolerance) + " ****")
        print()
        print("** Simulating with strategy: Random **")
        start = time.time()
        result = simulate(graph.copy(), initial_loads, spaths, tolerance, remove_random)
        end = time.time()
        simulation_results1.append(result)
        print(">>Took " + seconds_to_time(end - start) + " to simulate.")

        print()
        print("** Simulating with strategy: Highest Degree **")
        initial_loads, spaths = num_spaths(graph)
        start = time.time()
        result = simulate(graph.copy(), initial_loads, spaths, tolerance, remove_highest_degree)
        end = time.time()
        simulation_results2.append(result)
        print(">>Took " + seconds_to_time(end - start) + " to simulate.")

        print()
        print("** Simulating with strategy: Highest Load **")
        initial_loads, spaths = num_spaths(graph)
        start = time.time()
        result = simulate(graph.copy(), initial_loads, spaths, tolerance, remove_highest_load)
        end = time.time()
        simulation_results3.append(result)
        print(">>Took " + seconds_to_time(end - start) + " to simulate.")

    write_simulation_info_to_file(graph_name, "random", simulation_results1)
    write_simulation_info_to_file(graph_name, "highest_degree", simulation_results2)
    write_simulation_info_to_file(graph_name, "highest_load", simulation_results3)

    return simulation_results1, simulation_results2, simulation_results3


if __name__ == "__main__":
    import sys
    import numpy as np
    from networks_generator import *
    #from plot_distribution import *

    print("****** INIT SIMULATIONS ******")
    graph_name = sys.argv[1]
    strategy = sys.argv[2]

    #### Load Network ####
    if graph_name == "diseasome":
        #graph = nx.read_adjlist("./networks/" + graph_name + ".csv")
        graph = nx.read_graphml("./networks/" + graph_name + ".graphml")
        graph = graph.to_undirected()
    else:
        graph = nx.read_gexf("./networks/" + graph_name + ".gexf")

    # start count simulation
    start = time.time()
    initial_loads, spaths = num_spaths(graph)

    #tolerances = np.arange(0.0, 1.1, 0.1)
    tolerances = np.arange(0.0, 1.1, 0.1)

    print(tolerances)
    # run all simulations
    if strategy == "all":
        result = all_simulatons(graph.copy(), initial_loads, spaths, tolerances, graph_name)
        print(result)
        # todo: join the results into a file


    print("****** END SIMULATIONS ******")
    # fazer com que o ficheiro dos plots leia o ficheiro gerado das simulacoes e converta para outro onde se possa ler
     #   "bem para fazer o plot