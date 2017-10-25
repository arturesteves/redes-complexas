import matplotlib.pyplot as plt

import csv
import sys

network_name = "diseasome"
x = 100
y = 100

if len(sys.argv) > 0:
	print sys.argv
	network_name = sys.argv[1]
if len(sys.argv) > 1:
	x = int(sys.argv[2])
if len(sys.argv) > 2:
	y = int(sys.argv[3])

x_list = []
y_list = []

with open('dataset_' + network_name + '.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in spamreader:
		x_list.append(int(row[0]))
		y_list.append(int(row[2]))

#lists = sorted(itertools.izip(*[x, y]))
#x_list, y_list = list(itertools.izip(*lists))

#x_list, y_list = zip(*sorted(zip(x_list, y_list)))
plt.plot(x_list, y_list)
plt.axis([0, x, 0, y])
plt.show()

