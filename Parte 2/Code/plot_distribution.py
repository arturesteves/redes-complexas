import numpy as np
import matplotlib.pyplot as plt
from pyparsing import *


def get_values_damaged_caused_by_attack(base_filename):
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


def get_values_damaged_caused_by_attack_special_format(base_filename, num_init_nodes, num_final_nodes, interval):
    num_nodes_simulation = np.arange(num_init_nodes, num_final_nodes + interval, interval)
    filenames = []
    for num_nodes in num_nodes_simulation:
        filenames.append(base_filename + "_" + str(num_nodes))

    _random = []
    _hdegree = []
    _hload = []
    for filename in filenames:
        with open("./generate_all/" + filename + ".txt", "r") as f:
            line = f.readline()
            enclosed = Forward()
            nestedParens = nestedExpr('[', ']', content=enclosed)
            enclosed << (Word(alphanums + '.') | ',' | nestedParens)
            all_lists = enclosed.parseString(line).asList()
            random = all_lists[0][0],   # dont delete comma
            hdegree = all_lists[0][2],
            hload = all_lists[0][4],

            _random.append(get_clean_list(random))
            _hdegree.append(get_clean_list(hdegree))
            _hload.append(get_clean_list(hload))

            print(_random)
    return _random, _hdegree, _hload


def get_clean_list(list):
    aux_values = []
    aux_ = []
    for i in range(0, 11, 2):
        # print("    " + str(list[0][i]))
        for j in range(0, 9, 2): # depois aqui tambem deve ficar 11 quando existir tudo
            # print("        " + str(list[0][i][j]))
            aux_values.append(list[0][i][j])
            aux_.append(aux_values)
        aux_values = []
    list = aux_
    return list


def list_average(_list):
    damaged_caused_average = []
    for i in range(len(_list)):
        print(_list)
        begin = 0
        end = 5
        for j in range(0, 3):
            print("    " + str(_list[i]))
            print("      ", [x for x in _list[i][begin:end]])
            lists_to_average = [row[4] for row in [x for x in _list[i][begin:end]]]
            print("          ", lists_to_average)
            # [row[4] for row in attack_values[0]]
            damaged_caused_average.append(sum(lists_to_average) / float(len(lists_to_average)))
            begin += end
            end += end

    return damaged_caused_average


def generate_plot(attack_values):
    ####
    t1 = [0.003, 0.997, 0.999, 0.999, 0.999, 0.999]
    t2 = [0.021, 0.043, 0.053, 0.266, 0.915, 0.963]
    t3 = [0.021, 0.043, 0.053, 0.266, 0.915, 0.963]
    t = [t1, t2, t3]

    y1 = [0.99784365079365082, 0.9917543650793651, 0.99871150793650794, 0.99295079365079364, 0.99911150793650794, 0.99914325396825396]

    y2 = [0.377239285714285714, 0.377239285714285714, 0.377239285714285714, 0.377239285714285714, 0.377239285714285714, 0.377239285714285714]
    y3 = y2 = [0.377239285714285714, 0.377239285714285714, 0.377239285714285714, 0.377239285714285714, 0.377239285714285714, 0.377239285714285714]
    y = [y1, y2, y3]
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
    #attack_values = get_values_damaged_caused_by_attack_special_format("result", 1000, 1800, 200)
    #print("attack\n " + str(attack_values))
    #print("Random: " + str(attack_values[0]))

    #print("average")
    #damage_random = list_average(attack_values[0])  # random
    #damaged_degree = list_average(attack_values[0])  # random
    #damaged_load = list_average(attack_values[0])  # random

    #generate_plot([damage_random, damaged_degree, damaged_load])

    # passar por todos os valores de attack_values[0], de 5 em 5 somar e calcular a media e depois fica o
    # valor da tolerancia 0, depois o mesmo processo para tolerancia 0.2


    #damaged_random = [row[4] for row in attack_values[0]]
    #damaged_degree = [row[4] for row in attack_values[1]]
    #damaged_load = [row[4] for row in attack_values[2]]

    #print("damaged_random: ", damaged_random)
#    print("damaged_degree: ", damaged_degree)
#    print("damaged_load: ", damaged_load)



    """
    attack_values = []
    attack_values.append(get_values_damaged_caused_by_attack("scalefree_1000"
                                                             "N_2AVD_removed_by_random_tolerance"))
    attack_values.append(get_values_damaged_caused_by_attack("scalefree_1000N_2AVD_removed_by_highest_"
                                                             "degree_tolerance"))
    attack_values.append(get_values_damaged_caused_by_attack("scalefree_1000N_2AVD_removed_by_highest_"
                                                             "load_tolerance"))

    damaged_random = [row[4] for row in attack_values[0]]
    damaged_degree = [row[4] for row in attack_values[1]]
    damaged_load = [row[4] for row in attack_values[2]]

    print("damaged_random: ", damaged_random)
    print("damaged_degree: ", damaged_degree)
    print("damaged_load: ", damaged_load)

    generate_plot(attack_values)
    """