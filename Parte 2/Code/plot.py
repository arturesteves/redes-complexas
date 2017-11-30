import numpy as np
import matplotlib.pyplot as plt
import sys


def get_simulation_result(basefilename):
    s = "_removed_by_"
    values = []
    filenames = [basefilename + s + "random", basefilename + s + "highest_degree", basefilename + s + "highest_load"]

    for file in filenames:
        with open("./data/" + file, "r") as f:
            values_aux = f.readlines()
            values.append([eval(x) for x in values_aux])

    # 1- random values; 2- highest degree values: 3- highest load values
    return values


def plot(values, filename_n1, filename_n2=""):
    tolerances = np.arange(0.0, 1.1, 0.1)
    style = ["-->", "-.^", ":<", "--^", "-.>", ":<"]
    #labels = ["random", "highest degree", "highest load"]
    labels = ["random - N1", "highest degree - N1", "highest load - N1",
              "random - N2", "highest degree - N2", "highest load - N2"]

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

    if filename_n2 == "":
        plt.title(filename_n1 + " N: " + str(values[0][0]["N"]))
    else:
        plt.title(filename_n1 + " N: " + str(values[0][0]["N"]) + "\n" +
                  filename_n2 + " N: " + str(values[3][0]["N"]))

    # Put a legend below current axis
    #plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
    #           fancybox=True, shadow=True, ncol=3)
    plt.legend(bbox_to_anchor=(1.0, 0.4))

    fig.savefig("./graphics/" + filename_n1 + "_" + filename_n2 + ".png")
    plt.show()


def plot_single(basefilename):
    values = get_simulation_result(basefilename)
    plot(values, basefilename)


def plot_double(basefilename_network1, basefilename_network2):
    values_network1 = get_simulation_result(basefilename_network1)
    values_network2 = get_simulation_result(basefilename_network2)
    values_network1.extend(values_network2)  # join the values of each network result
    plot(values_network1, basefilename_network1, basefilename_network2)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        plot_single(sys.argv[1])
    elif len(sys.argv) == 3:
        plot_double(sys.argv[1], sys.argv[2])
    else:
        raise ValueError("You need to pass the name of the base file of the simulation results.")
