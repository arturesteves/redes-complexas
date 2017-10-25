import matplotlib.pyplot as plt

import csv
import sys

network_name = "diseasome"
x = 100
y = 100

m = 0

if len(sys.argv) > 1:
    print sys.argv
    network_name = sys.argv[1]
if len(sys.argv) > 2:
    x = int(sys.argv[2])
if len(sys.argv) > 3:
    y = int(sys.argv[3])
if len(sys.argv) > 4:
    m = float(sys.argv[4])

x_list = []
y_list = []
d_list = []

with open('dataset_' + network_name + '.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        x_list.append(int(row[0]))
        y_list.append(int(row[2]))
        if m:
            d_list.append(m * int(row[0]) + 5200)

# lists = sorted(itertools.izip(*[x, y]))
# x_list, y_list = list(itertools.izip(*lists))

# x_list, y_list = zip(*sorted(zip(x_list, y_list)))
plt.plot(x_list, y_list)
if m:
    plt.plot(x_list, d_list)
plt.axis([0, x, 0, y])
plt.show()
