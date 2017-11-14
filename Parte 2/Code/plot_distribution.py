import numpy as np
import matplotlib.pyplot as plt


def get_values_of_damaged_caused_by_attack(base_filename):
    tolerances = np.arange(0.0, 1.2, 0.2)
    filenames = []
    for tolerance in tolerances:
        filenames.append(base_filename + "_" + str(tolerance))

    values = []

    for filename in filenames:
        with open("./output/" + filename + ".txt", "r") as f:
            line = f.readline().replace("[", "")
            line = line.replace("]", "")
            line = line.split(", ")
            values.append([float(number) for number in line])

    return values


def generate_plot(attack_values):
    ####
    t1 = [0.003, 0.997, 0.999, 0.999, 0.999, 0.999]
    t2 = [0.021, 0.043, 0.053, 0.266, 0.915, 0.963]
    t3 = [0.021, 0.043, 0.053, 0.266, 0.915, 0.963]
    t = [t1, t2, t3]
    ####
    tolerances = np.arange(0.0, 1.2, 0.2)
    style = ["--", "-.", ":"]
    marker = ["^", ".", ""]
    labels = ["random", "highest degree", "highest load"]

    fig = plt.figure()
    ax = plt.subplot(111)

    index = 0
    for i in attack_values:
        damaged = [row[4] for row in attack_values[index]]
        plot = ax.plot(tolerances, damaged, style[index], label=labels[index])
        # plot = ax.errorbar(x_list, i, 0.05, linestyle=style[index], marker=marker[index])
        index += 1

    # Put a legend below current axis
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
               fancybox=True, shadow=True, ncol=5)

    plt.show()


if __name__ == "__main__":
    attack_values = []
    attack_values.append(get_values_of_damaged_caused_by_attack("scalefree_1000"
                                                                "N_2AVD_removed_by_random_tolerance"))
    attack_values.append(get_values_of_damaged_caused_by_attack("scalefree_1000N_2AVD_removed_by_highest_"
                                                                "degree_tolerance"))
    attack_values.append(get_values_of_damaged_caused_by_attack("scalefree_1000N_2AVD_removed_by_highest_"
                                                                "load_tolerance"))

    damaged_random = [row[4] for row in attack_values[0]]
    damaged_degree = [row[4] for row in attack_values[1]]
    damaged_load = [row[4] for row in attack_values[2]]

    print("damaged_random: ", damaged_random)
    print("damaged_degree: ", damaged_degree)
    print("damaged_load: ", damaged_load)

    generate_plot(attack_values)
