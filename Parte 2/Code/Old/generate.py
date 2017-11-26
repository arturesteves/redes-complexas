import networkx as nx
from random import randint
import pickle
import time
import copy


# todo remove paths to themselves

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


#################################
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

                # test:
    # print("a", graph.nodes())
    # for source in list(spaths):
    # 	print("b", list(spaths[source]))
    # 	for target in list(spaths[source]):
    # 		if target not in graph.nodes():
    # 			print('not in')

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
    print("Node Removed")
    cascade(graph, initial_loads, spaths, tolerance, index)


# removes a node by highest load and cascades
def remove_highest_load(graph, initial_loads, spaths, tolerance):
    index = max(initial_loads, key=initial_loads.get)
    graph.remove_node(index)
    print("Node Removed")
    cascade(graph, initial_loads, spaths, tolerance, index)


# simulates the removal of a node and calculates the cascading effect
def simulate(graph, initial_loads, spaths, tolerance, removal_function, filename):
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

    with open("./output/" + filename + ".txt", "w") as f:
        f.write(str([tolerance, N, nx.number_of_nodes(graph), N_prime, G]))

    return [tolerance, nx.number_of_nodes(graph), N, N_prime, G]


print("Reading graph from file")
#graph_name = "graph_scalefree_2000_1"
graph_name = "scalefree_1000N_2AVD"
graph = nx.read_gpickle("./networks/" + graph_name + ".gpickle")
print("Calculating shortest paths and initial loads")
initial_loads, spaths = num_spaths(graph)

# run the simulation for each tolerance value
simulation_results1 = []
simulation_results2 = []
simulation_results3 = []

for tolerance in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
    print("**** Simulating with tolerance: " + str(tolerance) + " ****")
    print("** Simulating with strategy: Random **")
    result = simulate(graph.copy(), initial_loads, spaths, tolerance, remove_random,
                      graph_name + "_" + str(graph.size()) + "_removed_by_random_tolerance_" + str(tolerance))
    simulation_results1.append(result)

    initial_loads, spaths = num_spaths(graph)

    print("** Simulating with strategy: Highest Degree **")
    result = simulate(graph.copy(), initial_loads, spaths, tolerance, remove_highest_degree,
                      graph_name + "_" + str(graph.size()) + "_removed_by_highest_degree_tolerance_" + str(tolerance))
    simulation_results2.append(result)

    initial_loads, spaths = num_spaths(graph)

    print("** Simulating with strategy: Highest Load **")
    result = simulate(graph.copy(), initial_loads, spaths, tolerance, remove_highest_load,
                      graph_name + "_" + str(graph.size()) + "_removed_by_highest_load_tolerance_" + str(tolerance))
    simulation_results3.append(result)

print([simulation_results1, simulation_results2, simulation_results3])
