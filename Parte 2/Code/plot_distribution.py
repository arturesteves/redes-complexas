import numpy as np
import matplotlib.pyplot as plt
from pyparsing import *


def get_values_damaged_caused_by_attack(base_filename):
    tolerances = np.arange(0.0, 1.2, 0.2)
    filenames = []
    for tolerance in tolerances:
        filenames.append(base_filename + "_" + str(tolerance))

    values = []





def generate_plot(filename):
    ####

    with open("./network/" + filename + , "r") as f:
        line = f.readline().replace("[", "")
        line = line.replace("]", "")
        line = line.split(", ")
        values.append([float(number) for number in line])




    ####
    tolerances = np.arange(0.0, 1.2, 0.2)
    style = ["--", "-.", ":"]
    marker = ["^", ".", ""]
    labels = ["random", "highest degree", "highest load"]

    fig = plt.figure()
    ax = plt.subplot(111)

    index = 0
    for i in y:
        #damaged = [row[4] for row in attack_values[index]]
        plot = ax.plot(tolerances, y[i], style[index], label=labels[index])
        # plot = ax.errorbar(x_list, i, 0.05, linestyle=style[index], marker=marker[index])
        index += 1

    # Put a legend below current axis
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
               fancybox=True, shadow=True, ncol=5)

    plt.show()


if __name__ == "__main__":
    generate_plot(None)
