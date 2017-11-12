import csv
import sys
import math

Y = []
X = []

x1 = None
x2 = None
network_name = None
SX = 0.0
SY = 0.0
SXX = 0.0
SXY = 0.0
SYY = 0.0
SumProduct = 0.0


if len(sys.argv) > 1:
    print sys.argv
    network_name = sys.argv[1]
if len(sys.argv) > 2:
    x1 = int(sys.argv[2])
if len(sys.argv) > 3:
    x2 = int(sys.argv[3])

if network_name is not None  and x1 is not None and x2 is not None:
    with open(network_name+'.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if int(row[0]) == 5000:
                break
            X.append(int(row[0]))
            Y.append(int(row[2]))

    N = len(X)

    for i in xrange(N):
        SX = SX + float(math.log(X[i]))
        SY = SY + float(Y[i])
        SXY = SXY + float(math.log(X[i])) * float(Y[i])
        SXX = SXX + float(math.log(X[i])) * float(math.log(X[i]))
        SYY = SYY + float(Y[i]) * float(Y[i])

    Slope = ((N * SXY) - (SX * SY)) / ((N * SXX) - (SX * SX))
    print Y[x1]
    print X[x1]
    print Y[x2]
    print X[x2]
    Slope = (float(Y[x2])-float(Y[x1])) / (float(X[x2])-float(X[x1]))
    print Slope

else :
    print("Invalid arguments")