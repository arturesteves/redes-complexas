import networkx as nx
from random import randint
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


# compute the number of shortest paths that pass through each node. Returns dict
def num_spaths(graph):
    start = time.time()
    n_spaths = dict.fromkeys(graph, 0.0)
    spaths = dict(nx.all_pairs_shortest_path(graph))
    #spaths = dict(nx.floyd_warshall(graph))

    for source in spaths:
        for path in spaths[source].items():
            for node in path[1][1:]:  # ignore first element (source == node)
                n_spaths[node] += 1  # this path passes through `node`

    end = time.time()
    elapsed_time = end - start
    print("It took " + seconds_to_time(elapsed_time) + " to compute the number of shortest paths that pass through each node.")
    return n_spaths


def cascade(graph, initial_loads, tolerance):
    start = time.time()
    stable = False
    while not stable:
        stable = True
        current_load = num_spaths(graph)
        for node_load in current_load.items():
            node = node_load[0]
            load = node_load[1]
            if load > (1 + tolerance) * initial_loads[node]:
                graph.remove_node(node)
                print("Node Removed by cascading")
                time_remove_node = time.time()
                elapsed = time_remove_node - start
                print("It took " + seconds_to_time(elapsed) + " to remove a node suffering from the cascade effect.")
                stable = False
                break

    end = time.time()
    elapsed_time = end - start
    print("It took " + seconds_to_time(elapsed_time) + " to complete the cascade effect.")


#
# this functions returns the list of nodes and the nodes that compose the shortest path
# between the source and target, but also return a list containing the nodes and the value of shortest
# paths that pass through the source node
def updated_num_spaths(graph):
    start = time.time()
    n_spaths = dict.fromkeys(graph, 0.0)
    spaths = dict(nx.all_pairs_shortest_path(graph))
    nodes_spaths_pass_through_nodes = {node: set() for node in graph.nodes}  # each node has a list of nodes that

    # count for each node the number of shortest paths it is in
    for source in spaths:
        for path in spaths[source].items():
            for node in path[1][1:]:  # ignore first element (source == node)
                n_spaths[node] += 1  # this path passes through `node`
                nodes_spaths_pass_through_nodes[source].add(node)

    end = time.time()
    elapsed_time = end - start
    print("It took " + seconds_to_time(elapsed_time) + " to compute the number of shortest paths that pass through each node.")

    return n_spaths, nodes_spaths_pass_through_nodes

#
#
def custom_num_spaths(graph, list_nodes):
    start = time.time()
    n_spaths = dict.fromkeys(graph, 0.0)
    spaths = {}  # empty dictionary
    nodes_spaths_pass_through_nodes = {node: set() for node in graph.nodes}  # each node has a list of nodes that

    for n in list_nodes:
        spaths[n] = nx.single_source_shortest_path(graph, n)

    # aqui nao sao tidos em conta os nos cujos os loads nao foram re-calculados
    for source in spaths:
        for path in spaths[source].items():
            for node in path[1][1:]:  # ignore first element (source == node)
                n_spaths[node] += 1  # this path passes through `node`
                nodes_spaths_pass_through_nodes[source].add(node)

    end = time.time()
    elapsed_time = end - start
    print("It took " + seconds_to_time(
        elapsed_time) + " to compute the number of shortest paths that pass through each node.")
    return n_spaths, nodes_spaths_pass_through_nodes


#
# optimization from the function under:
# computes only the number of shortest paths that pass through each node
# that are affected when nodes are removed
def optimized_cascade(graph, initial_loads, tolerance):
    start = time.time()
    stable = False
    current_load, nodes_spaths_pass_through_nodes = updated_num_spaths(graph)
    affected_nodes = set()  # nodes that need to recalculate the shortest paths
    while not stable:
        stable = True
        # recompute current_load
        print("old: ", current_load)

        # o merge so pode acontecer se o valor nao for zero, isto do if len nao funciona para sempre
        if len(affected_nodes) > 0:  # if are nodes affected
            new_current_load, nodes_spaths_pass_through_nodes = custom_num_spaths(graph, affected_nodes)
            # necessario fazer merge de nodes_spaths_ ... tambem, mas aqui o merge, nao e substituir é fazer append

            # merge lists  # the old values of the nodes need to change, dictionary like..
            print("new: ", new_current_load)
            current_load = {**current_load, **new_current_load}  # merge dictionaries, to update the new loads of the nodes affected
            # em principio do merge deve ser preciso retirar alguns nos - os que entretanto foram removidos pelo cascading?

        print("merged: ", current_load)
        for node_load in current_load.items():
            node = node_load[0]
            load = node_load[1]
            if load > (1 + tolerance) * initial_loads[node]:  # check if node was affected
                graph.remove_node(node)
                # obter a lista dos nos cujo shortest path passava por node.
                affected_nodes.update(nodes_spaths_pass_through_nodes[node])  # update set

                current_load.pop(node, None)  # remove the node from being used
                # the node removed must be removed from the lists in which it might be in

                print("Node Removed by cascading: " + str(node))
                time_remove_node = time.time()
                elapsed = time_remove_node - start
                print("It took " + seconds_to_time(elapsed) + " to remove a node suffering from the cascade effect.")
                stable = False
                break

        affected_nodes.clear()

    end = time.time()
    elapsed_time = end - start
    print("It took " + seconds_to_time(elapsed_time) + " to complete the cascade effect.")


# removes a random node and cascades
def remove_random(graph, initial_loads, tolerance):
    nodes = list(graph.nodes())
    index = randint(0, len(nodes) - 1)
    graph.remove_node(nodes[index])
    print("Node Removed: " + str(nodes[index]))
    #cascade(graph, initial_loads, tolerance)
    optimized_cascade(graph, initial_loads, tolerance)


# removes a node by highest degree and cascades
def remove_highest_degree(graph, initial_loads, tolerance):
    nodes = list(graph.nodes())
    degrees = dict(graph.degree())
    index = max(degrees, key=degrees.get)
    graph.remove_node(nodes[index])
    print("Node Removed")
    cascade(graph, initial_loads, tolerance)


# removes a node by highest load and cascades
def remove_highest_load(graph, initial_loads, tolerance):
    nodes = list(graph.nodes())
    index = max(initial_loads, key=initial_loads.get)
    graph.remove_node(nodes[index])
    print("Node Removed")
    cascade(graph, initial_loads, tolerance)


# simulates the removal of a node and calculates the cascading effect
def simulate(graph, tolerance, removal_function, filename):
    initial_loads = num_spaths(graph)

    # calculate the size of the giant component  before removing
    component_sizes = list(map(lambda sg: nx.number_of_nodes(sg), list(nx.connected_component_subgraphs(graph))))
    N = max(component_sizes) if len(component_sizes) > 0 else 0

    # remove the node and cascade
    removal_function(graph, initial_loads, tolerance)

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

    with open(filename + ".txt", "w") as f:
        f.write(str([tolerance, nx.number_of_nodes(graph), N_prime, G]))

    return [tolerance, nx.number_of_nodes(graph), N_prime, G]


graph = nx.read_gpickle("./graph_scalefree_5000.txt")

# run the simulation for each tolerance value
simulation_results = []
#for tolerance in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
for tolerance in [0.6, 0.8, 1.0]:
    print("**** Simulating with tolerance: " + str(tolerance) + " ****")
    print("** Simulating with strategy: Random **")
    result = simulate(graph.copy(), tolerance, remove_random,
                      "scale_free_5000_removed_by_random_tolerance_" + str(tolerance))
    simulation_results.append(result)
    print("** Simulating with strategy: Highest Degree **")
    result = simulate(graph.copy(), tolerance, remove_highest_degree,
                      "scale_free_5000_removed_by_highest_degree_tolerance_" + str(tolerance))
    simulation_results.append(result)
    print("** Simulating with strategy: Highest Load **")
    result = simulate(graph.copy(), tolerance, remove_highest_load,
                      "scale_free_5000_removed_by_highest_load_tolerance_" + str(tolerance))
    simulation_results.append(result)

print(simulation_results)
