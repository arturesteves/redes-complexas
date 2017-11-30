import numpy as np
import matplotlib.pyplot as plt
import sys

def get_simulation_result(basefilename):
    s = "_removed_by_"
    values = []
    filenames = [basefilename + s + "random", basefilename + s + "highest_degree", basefilename + s + "highest load"]

    for file in filenames:
        with open("./data/" + file, "r") as f:
            values_aux = f.readlines()
            values.append([eval(x) for x in values_aux])

    # 1- random values; 2- highest degree values: 3- highest load values
    return values


def generate_plot(basefilename):
    values = get_simulation_result(basefilename)
    #random_G = [x["G"] for x in values[0]]
    #highest_degree_G = [x["G"] for x in values[1]]
    #highest_load_G = [x["G"] for x in values[2]]

    #t = [random_G, highest_degree_G, highest_load_G]
    # {'tolerance:': 0.0, 'graph-size': 1084, 'N: ': 1000, 'N_prime': 672, 'G: ': 0.672}
    ####
    tolerances = np.arange(0.0, 1.1, 0.1)
    style = ["--", "-.", ":"]
    marker = ["^", ".", ""]
    labels = ["random", "highest degree", "highest load"]

    fig = plt.figure()
    ax = plt.subplot(111)
    axes = plt.gca()
    axes.set_xlim([0.0, 1.05])
    axes.set_ylim([0.0, 1.05])

    index = 0
    for val in values:
        r = [x["G"] for x in val]
        plot = ax.plot(tolerances, r, style[index], label=labels[index])
        index += 1

    # Put a legend below current axis
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
               fancybox=True, shadow=True, ncol=5)
    fig.savefig("./graphics/" + basefilename + ".png")
    plt.show()


if __name__ == "__main__":
    #generate_plot("scalefree_network_with_central_cluster_3")
    if len(sys.argv) > 1:
        generate_plot(sys.argv[1])
    else:
        raise ValueError("You need to pass the name of the base file of the simulation results.")
